from autonomous_driving_manager import AutonomousDrivingState
from Commands.commands import NameValueTuple, InfoList
from Config.config import Config
from datetime import datetime
import shelve
import cv2
import os


class CarStateData:
    def __init__(self, config: Config):
        self.autonomous_mode = False
        self.autonomous_driving_state: AutonomousDrivingState = None
        self.sonar_value = 101
        self.motor_power_value = 0
        self.steering_value = config.steering_servo_range[1]
        self.debug_values = dict()

    def load_from_dict(self, d: dict):
        self.sonar_value = d['sonar_value']
        self.motor_power_value = d['motors_power_values']
        self.steering_value = d['steering_value']
        self.debug_values = d['debug_values']

    def to_dict(self) -> dict:
        d = dict()
        d['sonar_value'] = self.sonar_value
        d['motors_power_values'] = self.motor_power_value
        d['steering_value'] = self.steering_value
        d['debug_values'] = self.debug_values
        return d


class CarState(object):
    def __init__(self, config: Config):
        self.config = config
        self.data = CarStateData(config=config)
        self.state_updated = False
        self._autonomous_state_subscribers = []
        self._sonar_subscribers = []
        self._motor_power_subscribers = []
        self._steering_subscribers = []
        self._state_recording_enabled = False
        self._state_records_dir = ''
        self._state_recording_shelve = None

    def update_state(self, info_event: NameValueTuple):
        if info_event.name == InfoList.AUTONOMOUS_DRIVING_STATE_UPDATED:
            self._call_autonomous_state_subscribers()

        elif info_event.name == InfoList.SONAR_VALUE_UPDATED:
            self.data.sonar_value = info_event.value
            self._call_sonars_data_subscribers()

        elif info_event.name == InfoList.MOTOR_VALUE_UPDATED:
            self.data.motor_power_value = info_event.value
            self._call_motor_power_subscribers()

        elif info_event.name == InfoList.STEERING_VALUE_UPDATED:
            self.data.steering_value = info_event.value
            self._call_steering_subscibers()

        elif info_event.name == InfoList.START_STOP_STATE_RECORDING:
            if self._state_recording_enabled:
                self._disable_state_recording()
            else:
                self._enable_state_recording()

        elif info_event.name == InfoList.SAVE_STATE:
            self._save_current_state(info_event.value)

        self.state_updated = True

    def _call_autonomous_state_subscribers(self):
        for hook in self._autonomous_state_subscribers:
            hook()

    def _call_sonars_data_subscribers(self):
        for hook in self._sonar_subscribers:
            hook()

    def _call_motor_power_subscribers(self):
        for hook in self._motor_power_subscribers:
            hook()

    def _call_steering_subscibers(self):
        for hook in self._steering_subscribers:
            hook()

    def subscribe_to_autonomous_state_changes(self, hook):
        self._autonomous_state_subscribers.append(hook)

    def subscribe_to_sonars_data_changes(self, hook):
        self._sonar_subscribers.append(hook)

    def subscribe_to_motors_power_changes(self, hook):
        self._motor_power_subscribers.append(hook)

    def subscribe_to_steering_value_changes(self, hook):
        self._steering_subscribers.append(hook)

    def _enable_state_recording(self):
        dir_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self._state_records_dir = os.path.join(self.config.states_records_dir, dir_name)
        os.mkdir(self._state_records_dir)
        self._state_recording_shelve = shelve.open(os.path.join(self._state_records_dir, 'car_state_data'))
        self._state_recording_enabled = True

    def _disable_state_recording(self):
        self._state_recording_enabled = False
        self._state_recording_shelve.sync()
        self._state_recording_shelve.close()

    def _save_current_state(self, frame):
        if self._state_recording_enabled:
            time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
            file_name = f'{os.path.join(self._state_records_dir, time)}.png'
            cv2.imwrite(file_name, frame)
            self._state_recording_shelve[time] = self.data.to_dict()
