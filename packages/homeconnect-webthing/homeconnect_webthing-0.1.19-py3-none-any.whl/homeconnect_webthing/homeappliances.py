import logging
import requests
import json
from abc import abstractmethod
from time import sleep
from threading import Thread
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from homeconnect_webthing.auth import Auth
from homeconnect_webthing.eventstream import EventListener, ReconnectingEventStream
from homeconnect_webthing.utils import print_duration



DRYER = 'dryer'
DISHWASHER = 'dishwasher'



def is_success(status_code: int) -> bool:
    return status_code >= 200 and status_code <= 299


class Appliance(EventListener):

    def __init__(self, device_uri: str, auth: Auth, name: str, device_type: str, haid: str, brand: str, vib: str, enumber: str):
        self._device_uri = device_uri
        self._auth = auth
        self.name = name
        self.device_type = device_type
        self.haid = haid
        self.brand = brand
        self.vib = vib
        self.enumber = enumber
        self.__value_changed_listeners = set()
        self.last_refresh = datetime.now() - timedelta(hours=9)
        self.remote_start_allowed = False
        self.program_remaining_time_sec = 0
        self.__program_selected = ""
        self._power = ""
        self._door = ""
        self._operation = ""


    @property
    def power(self):
        if len(self._power) > 0:
            return self._power[self._power.rindex('.')+1:]

    @property
    def door(self):
        if len(self._door) > 0:
            return self._door[self._door.rindex('.')+1:]
        else:
            return ""

    @property
    def operation(self):
        if len(self._operation)> 0:
            return self._operation[self._operation.rindex('.')+1:]
        else:
            return ""

    @property
    def program_selected(self):
        if len(self.__program_selected) > 0:
            return self.__program_selected[self.__program_selected.rindex('.')+1:]
        else:
            return ""

    @abstractmethod
    def read_start_date(self) -> str:
        pass

    @abstractmethod
    def write_start_date(self, dt: str):
        pass

    def register_value_changed_listener(self, value_changed_listener):
        self.__value_changed_listeners.add(value_changed_listener)
        self.__notify_listeners()

    def __notify_listeners(self):
        for value_changed_listener in self.__value_changed_listeners:
            value_changed_listener()

    def on_connected(self):
        logging.info("refresh " + self.name + " state (new event stream connection)")
        self._refresh(reason="on connected")

    def on_keep_alive_event(self, event):
        logging.debug("keep alive event")

    def on_notify_event(self, event):
        logging.debug("notify event: " + str(event.data))
        self._on_value_changed_event(event)

    def on_status_event(self, event):
        logging.debug("status event: " + str(event.data))
        self._on_value_changed_event(event)

    def _on_event_event(self, event):
        logging.debug("event event: " + str(event.data))
        pass

    def _on_value_changed_event(self, event):
        if event.id == self.haid:
            try:
                data = json.loads(event.data)
                self._on_values_changed(data.get('items', []), "updated")
                self.__notify_listeners()
            except Exception as e:
                logging.warning("error occurred by handling event " + str(event), e)

    def _on_values_changed(self, changes: List[Any], ops: str = "updated"):
        for record in changes:
            key = record.get('key', "")
            value =  record.get('value', None)
            if value is None:
                logging.warning("key with One value " + key)
            else:
                if key == 'BSH.Common.Status.DoorState':
                    self._door = value
                    logging.info(self.name + " door state " + ops + ": " + str(self._door))
                elif key == 'BSH.Common.Status.OperationState':
                    self._operation = value
                    logging.info(self.name + " operation state " + ops + ": " + str(self._operation))
                elif key == 'BSH.Common.Status.RemoteControlStartAllowed':
                    self.remote_start_allowed = value
                    logging.info(self.name + " remote start allowed " + ops + ": " + str(self.remote_start_allowed))
                elif key == 'BSH.Common.Setting.PowerState':
                    self._power = value
                    logging.info(self.name + " power state " + ops + ": " + str(self._power))
                elif key == 'BSH.Common.Option.RemainingProgramTime':
                    self.program_remaining_time_sec = value
                elif key == 'BSH.Common.Root.SelectedProgram':
                    self.__program_selected = value
                else:
                    self._do_on_value_changed(key, value, ops)

    @abstractmethod
    def _do_on_value_changed(self, key: str, value: str, ops: str):
        return False

    def _refresh(self, notify: bool = True, reason: str = None):
        self.last_refresh = datetime.now()
        try:
            self._do_refresh(reason)
            if notify:
                self.__notify_listeners()
        except Exception as e:
            logging.warning("error occurred on refreshing", e)

    @abstractmethod
    def _do_refresh(self, reason: str = None):
        pass

    def _perform_get(self, path:str, raise_error: bool = True, ignore_error_codes: List[int] = None) -> Dict[str, Any]:
        uri = self._device_uri + path
        #logging.info("query GET " + uri)
        response = requests.get(uri, headers={"Authorization": "Bearer " + self._auth.access_token}, timeout=5000)
        if is_success(response.status_code):
            return response.json()
        else:
            if ignore_error_codes is None or response.status_code not in ignore_error_codes:
                logging.warning("error occurred by calling GET " + uri)
                logging.warning("got " + str(response.status_code) + " " + response.text)
                if raise_error:
                    raise Exception("error occurred by calling GET " + uri + " Got " + str(response))
            return {}

    def _perform_put(self, path:str, data: str, max_trials: int = 3, current_trial: int = 1):
        uri = self._device_uri + path
        response = requests.put(uri, data=data, headers={"Content-Type": "application/json", "Authorization": "Bearer " + self._auth.access_token}, timeout=5000)
        if not is_success(response.status_code):
            logging.warning("error occurred by calling PUT " + uri + " " + data)
            logging.warning("got " + str(response.status_code) + " " + str(response.text))
            if current_trial <= max_trials:
                delay = 1 + current_trial
                logging.warning("waiting " + str(delay) + " sec for retry")
                sleep(delay)
                self._perform_put(path, data, max_trials, current_trial+1)

    @property
    def __fingerprint(self) -> str:
        return self.device_type + ":" + self.brand + ":" + self.vib + ":" + self.enumber + ":" + self.haid

    def __hash__(self):
        return hash(self.__fingerprint)

    def __lt__(self, other):
        return self.__fingerprint < other.__fingerprint

    def __eq__(self, other):
        return self.__fingerprint == other.__fingerprint



class Dishwasher(Appliance):

    def __init__(self, device_uri: str, auth: Auth, name: str, device_type: str, haid: str, brand: str, vib: str, enumber: str):
        self.__program_start_in_relative_sec = 0
        self.__program_progress = 0
        self.__program_active = ""
        self.__program_remote_control_active = ""
        self.program_extra_try = ""
        self.program_hygiene_plus = ""
        self.program_vario_speed_plus = ""
        self.program_energy_forecast_percent = 0
        self.program_water_forecast_percent = 0
        super().__init__(device_uri, auth, name, device_type, haid, brand, vib, enumber)
        self._refresh(reason="dishwasher appliance initialized")

    def _do_on_value_changed(self, key: str, value: str, ops: str):
        if key ==  'BSH.Common.Root.ActiveProgram':
            self.__program_active = value
        elif key == 'BSH.Common.Option.StartInRelative':
            self.__program_start_in_relative_sec = value
        elif key == 'BSH.Common.Option.ProgramProgress':
            self.__program_progress = value
        elif key == 'BSH.Common.Status.RemoteControlActive':
            self.__program_remote_control_active = value
        elif key == 'Dishcare.Dishwasher.Option.ExtraDry':
            self.program_extra_try = value
        elif key == 'Dishcare.Dishwasher.Option.HygienePlus':
            self.program_hygiene_plus =value
        elif key == 'Dishcare.Dishwasher.Option.VarioSpeedPlus':
            self.program_vario_speed_plus = value
        elif key == 'BSH.Common.Option.EnergyForecast':
            self.program_energy_forecast_percent = value
        elif key == 'BSH.Common.Option.WaterForecast':
            self.program_water_forecast_percent = value
        else:
            logging.info("unhandled " + key + " -> " + value)

    def _do_refresh(self, reason: str = None):
        logging.info("fetch " + self.name + " settings, status and selection" + ("" if reason is None else " (" + reason +")"))
        settings = self._perform_get('/settings', raise_error=False)['data']['settings']
        logging.info("settings, status and selection fetched")
        self._on_values_changed(settings, "fetched")

        status = self._perform_get('/status', raise_error=False)['data']['status']
        self._on_values_changed(status, "fetched")

        record = self._perform_get('/programs/selected', raise_error=False)['data']
        self.__program_selected = record['key']
        self._on_values_changed(record.get('options', {}), "fetched")

        record = self._perform_get('/programs/active', raise_error=False, ignore_error_codes=[404]).get('data', {})
        self._on_values_changed(record.get('options', {}), "fetched")

    @property
    def program_progress(self):
        if self.operation.lower() == 'run':
            return self.__program_progress
        else:
            return 0

    def read_start_date(self) -> str:
        start_date = datetime.now() + timedelta(seconds=self.__program_start_in_relative_sec)
        if start_date > datetime.now():
            return start_date.strftime("%Y-%m-%dT%H:%M")
        else:
            return ""

    def write_start_date(self, dt: str):
        self._refresh(notify=False, reason="startdate updated pre-refresh")

        if self._operation in ["BSH.Common.EnumType.OperationState.Ready"]:
            remaining_secs_to_wait = int((datetime.fromisoformat(dt) - datetime.now()).total_seconds())
            if remaining_secs_to_wait < 0:
                logging.warning("negative delay " + str(remaining_secs_to_wait) + " (start date: " + dt + ") delay set to 5 sec")
                remaining_secs_to_wait = 5
            if remaining_secs_to_wait > 86000:
                logging.warning("large delay " + str(remaining_secs_to_wait) + " (start date: " + dt + ") reduced to 86000")
                remaining_secs_to_wait = 86000

            data = {
                "data": {
                    "key": self.__program_selected,
                    "options": [{
                                    "key": "BSH.Common.Option.StartInRelative",
                                    "value": remaining_secs_to_wait,
                                    "unit": "seconds"
                                }]
                }
            }
            try:
                self._perform_put("/programs/active", json.dumps(data, indent=2), max_trials=3)
                logging.info(self.name + " program " + self.program_selected + " starts in " + print_duration(remaining_secs_to_wait))
            except Exception as e:
                logging.warning("error occurred by starting " + self.name, e)
        else:
            logging.warning("ignoring start command. " +self.name + " is in state " + self._operation)
        self._refresh(reason="start date updated post-refresh")




class Dryer(Appliance):

    def __init__(self, device_uri: str, auth: Auth, name: str, device_type: str, haid: str, brand: str, vib: str, enumber: str):
        self.__program_finish_in_relative_sec = 0
        super().__init__(device_uri, auth, name, device_type, haid, brand, vib, enumber)
        self._refresh(reason="dryer appliance initialized")

    def _do_on_value_changed(self, key: str, value: str, ops: str):
        logging.info("unhandled " + key + " -> " + value)

    def _do_refresh(self, reason: str = None):
        logging.info("fetch settings, status and selection" + ("" if reason is None else " (" + reason +")"))
        settings = self._perform_get('/settings', raise_error=False)['data']['settings']
        logging.info("settings, status and selection fetched")
        self._on_values_changed(settings, "fetched")

        status = self._perform_get('/status', raise_error=False)['data']['status']
        self._on_values_changed(status, "fetched")

        record = self._perform_get('/programs/selected', raise_error=False)['data']
        self.__program_selected = record['key']
        self._on_values_changed(record.get('options', {}), "fetched")

        record = self._perform_get('/programs/active', raise_error=False, ignore_error_codes=[404]).get('data', {})
        self._on_values_changed(record.get('options', {}), "fetched")

    def read_start_date(self) -> str:
        start_date = datetime.now() + timedelta(seconds=self.__program_finish_in_relative_sec) - timedelta(seconds=self.program_remaining_time_sec)
        if start_date > datetime.now():
            return start_date.strftime("%Y-%m-%dT%H:%M")
        else:
            return ""

    def write_start_date(self, dt: str):
        self._refresh(notify=False, reason="start date updated pre-refresh")

        if self._operation in ["BSH.Common.EnumType.OperationState.Ready", '']:
            remaining_secs_to_wait = int((datetime.fromisoformat(dt) - datetime.now()).total_seconds()) + self.program_remaining_time_sec
            if remaining_secs_to_wait < 0:
                remaining_secs_to_wait = 5
            if remaining_secs_to_wait > 86000:
                logging.warning("large delay " + str(remaining_secs_to_wait) + " (start date: " + dt + ") reduced to 86000")
                remaining_secs_to_wait = 86000

            data = {
                "data": {
                    "key": self.__program_selected,
                    "options": [{
                        "key": "BSH.Common.Option.FinishInRelative",
                        "value": remaining_secs_to_wait,
                        "unit": "seconds"
                    }]
                }
            }
            try:
                self._perform_put("/programs/active", json.dumps(data, indent=2), max_trials=3)
                logging.info(self.name + " program " + "self.program_selected" + " starts in " + print_duration(remaining_secs_to_wait))
            except Exception as e:
                logging.warning("error occurred by starting " + self.name, e)
        else:
            logging.warning("ignoring start command. " + self.name + " is in state " + self._operation)
        self._refresh(reason="start date updated post-refresh")



def create_appliance(uri: str, auth: Auth, name: str, device_type: str, haid: str, brand: str, vib: str, enumber: str) -> Appliance:
    if device_type.lower() == DISHWASHER:
        return Dishwasher(uri, auth, name, device_type, haid, brand, vib, enumber)
    elif device_type.lower() == DRYER:
        return Dryer(uri, auth, name, device_type, haid, brand, vib, enumber)
    else:
        return Appliance(uri, auth, name, device_type, haid, brand, vib, enumber)



class HomeConnect:

    API_URI = "https://api.home-connect.com/api"

    def __init__(self, refresh_token: str, client_secret: str):
        self.notify_listeners: List[EventListener] = list()
        self.auth = Auth(refresh_token, client_secret)
        Thread(target=self.__start_consuming_events, daemon=True).start()

    # will be called by a background thread
    def __start_consuming_events(self):
        sleep(5)
        ReconnectingEventStream(HomeConnect.API_URI + "/homeappliances/events",
                                self.auth,
                                self,
                                read_timeout_sec=3*60,
                                max_lifetime_sec=90*60).consume()

    def on_connected(self):
        for notify_listener in self.notify_listeners:
            notify_listener.on_connected()

    def on_disconnected(self):
        for notify_listener in self.notify_listeners:
            notify_listener.on_disconnected()

    def on_keep_alive_event(self, event):
        for notify_listener in self.notify_listeners:
            notify_listener.on_keep_alive_event(event)

    def on_notify_event(self, event):
        for notify_listener in self.notify_listeners:
            notify_listener.on_notify_event(event)

    def on_status_event(self, event):
        for notify_listener in self.notify_listeners:
            notify_listener.on_status_event(event)

    def on_event_event(self, event):
        for notify_listener in self.notify_listeners:
            notify_listener.on_event_event(event)

    def appliances(self) -> List[Appliance]:
        uri = HomeConnect.API_URI + "/homeappliances"
        logging.info("requesting " + uri)
        response = requests.get(uri, headers={"Authorization": "Bearer " + self.auth.access_token}, timeout=5000)
        if is_success(response.status_code):
            data = response.json()
            devices = list()
            for homeappliances in data['data']['homeappliances']:
                device = create_appliance(HomeConnect.API_URI + "/homeappliances/" + homeappliances['haId'],
                                          self.auth,
                                          homeappliances['name'],
                                          homeappliances['type'],
                                          homeappliances['haId'],
                                          homeappliances['brand'],
                                          homeappliances['vib'],
                                          homeappliances['enumber'])
                self.notify_listeners.append(device)
                devices.append(device)
            return devices
        else:
            logging.warning("error occurred by calling GET " + uri)
            logging.warning("got " + str(response.status_code) + " " + response.text)
            raise Exception("error occurred by calling GET " + uri + " Got " + str(response))

    def dishwashers(self) -> List[Dishwasher]:
        return [device for device in self.appliances() if isinstance(device, Dishwasher)]

    def dishwasher(self) -> Optional[Dishwasher]:
        dishwashers = self.dishwashers()
        if len(dishwashers) > 0:
            return dishwashers[0]
        else:
            return None

    def dryers(self) -> List[Dryer]:
        return [device for device in self.appliances() if isinstance(device, Dryer)]

    def dryer(self) -> Optional[Dryer]:
        dryers = self.dryers()
        if len(dryers) > 0:
            return dryers[0]
        else:
            return None

