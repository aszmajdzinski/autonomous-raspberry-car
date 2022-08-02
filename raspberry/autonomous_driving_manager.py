from queue import Queue
from threading import Lock
from typing import Optional

from AutonomousDrivingMethods import ExampleAutonomousDrivingClass, \
    LaneInTheMiddleLinesDetection, LaneInTheMiddleBlobDetectionProportional
from AutonomousDrivingMethods.autonomous_driving import AutonomousDrivingState
from Commands.commands import NameValueTuple
from Hardware.camera import Camera


class AutonomousDrivingManager:
    def __init__(self, hardware_commands_queue: Queue, info_queue: Queue, image_queue: Queue,
                 car_state_data_path: str = None,
                 lock: Optional[Lock] = None):
        self.camera = Camera(resolution=(320, 240), framerate=15, rotation=180, car_state_data_path=car_state_data_path)
        self.camera.initialize_camera()
        self.hardware_commands_queue = hardware_commands_queue
        self.info_queue = info_queue
        self.method_args = (self._send_command, self._send_info, self.camera, image_queue, lock)
        self._methods = [ExampleAutonomousDrivingClass(*self.method_args),
                         LaneInTheMiddleLinesDetection(*self.method_args),
                         LaneInTheMiddleBlobDetectionProportional(*self.method_args)
                         ]
        self.state = AutonomousDrivingState()
        self._set_default_states()

    def _set_default_states(self):
        self.state.methods_names = self.methods_names
        self.select_method(0, activate=False)

    def select_method(self, index: int, activate=True):
        if 0 <= index < len(self._methods):
            self.disable_driving()
            self.selected_method.deactivate()
            self.state.selected_method_index = index
            self.state.selected_method_parameters = self.selected_method.parameters
            self.select_parameter(0)
            if activate:
                self.selected_method.activate()

    @property
    def methods_names(self) -> list:
        return [method.name for method in self._methods]

    @property
    def selected_method(self):
        return self._methods[self.state.selected_method_index]

    def select_parameter(self, index: int):
        self.state.select_parameter(index)

    def select_parameter_value_index(self, parameter_index: int, parameter_value_index: int):
        self.selected_method.set_parameter_value_index(parameter_index, parameter_value_index)

    def activate_autonomous_driving_mode(self):
        self.selected_method.activate()

    def deactivate_autonomous_driving_mode(self):
        self.selected_method.deactivate()

    def enable_driving(self):
        if not self.state.is_driving_enabled:
            self.state.is_driving_enabled = True
            self.selected_method.enable_driving()

    def disable_driving(self):
        self.selected_method.disable_driving()
        self.state.is_driving_enabled = False

    def shutdown(self):
        self.disable_driving()

    def _send_command(self, hardware_command: NameValueTuple):
        if self.state.is_driving_enabled:
            self.hardware_commands_queue.put(hardware_command)

    def _send_info(self, info: NameValueTuple):
        self.info_queue.put(info)
