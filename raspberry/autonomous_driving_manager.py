from queue import Queue
from threading import Lock
from typing import Optional

from AutonomousDrivingMethods import AnotherExampleAutonomousDrivingClass, ExampleAutonomousDrivingClass, \
    TrailFollower, LaneInTheMiddle
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
                         AnotherExampleAutonomousDrivingClass(*self.method_args),
                         TrailFollower(*self.method_args),
                         LaneInTheMiddle(*self.method_args),
                         ]
        self.state = AutonomousDrivingState()
        self._set_default_states()

    def _set_default_states(self):
        self.state.methods_names = self.methods_names
        self.select_method(0)

    def select_method(self, index):
        self.stop()
        if 0 <= index < len(self._methods):
            self.state.selected_method_index = index
            self.state.selected_method_parameters = self.selected_method.parameters
            self.select_parameter(0)

    @property
    def methods_names(self) -> list:
        m = []
        for method in self._methods:
            m.append(method.name)
        return m

    @property
    def selected_method(self):
        return self._methods[self.state.selected_method_index]

    def select_parameter(self, index: int):
        self.state.select_parameter(index)

    def select_parameter_value_index(self, parameter_index: int, parameter_value_index: int):
        self.selected_method.set_parameter_value_index(parameter_index, parameter_value_index)

    def start(self):
        if not self.state.is_active:
            self.state.is_active = True
            self.selected_method.start()

    def stop(self):
        if self.state.is_active:
            self.selected_method.stop()
            self.state.is_active = False

    def shutdown(self):
        self.stop()

    def _send_command(self, hardware_command: NameValueTuple):
        if self.state.is_active:
            self.hardware_commands_queue.put(hardware_command)

    def _send_info(self, info: NameValueTuple):
        if self.state.is_active:
            self.info_queue.put(info)
