from abc import ABC, abstractmethod
from dataclasses import dataclass
from queue import Queue
from threading import Thread, Lock
from time import time

import numpy

from Commands.commands import NameValueTuple, InfoList, HardwareCommandList
from Hardware.camera import Camera


class AutonomousDrivingAbstractClass(ABC):
    def __init__(self, command_call: callable, info_call: callable, camera: Camera, image_queue: Queue, lock: Lock):
        self.name = 'NoName Autonomous Driving Method'
        self.parameters = []
        self.camera = camera
        self.frame = None
        self._image_queue = image_queue
        self.lock = lock
        self._send_hardware_command = command_call
        self._send_info = info_call
        self._new_frame = False
        self._enabled = False
        self._worker_thread = None
        self._previous_frame_read_time = time()

    def set_parameter_value_index(self, parameter_index: int, selected_value_index: int):
        if self._is_parameter_index_valid(parameter_index):
            self.parameters[parameter_index].set_current_value_index(selected_value_index)

    def _is_parameter_index_valid(self, parameter_index: int) -> bool:
        return 0 <= parameter_index < len(self.parameters)

    def start(self):
        if not self._enabled:
            self._enabled = True
            self._worker_thread = Thread(target=self._worker)
            self._worker_thread.start()

    def stop(self):
        if self._enabled:
            self._enabled = False
            self._worker_thread.join()

    @abstractmethod
    def _process_frame(self):
        pass

    def _prepare(self):
        pass

    def _cleanup(self):
        pass

    def _worker(self):
        self._prepare()
        while self._enabled:
            self.frame = self.camera.grab_frame()
            self._show_image('Camera', self.frame)
            self._send_info(NameValueTuple(name=InfoList.SAVE_STATE, value=self.frame))
            self._process_frame()
            self._send_fps_debug()
        self._cleanup()
        self._stop_motors()
        self._steer(0)

    def _accelerate(self, value: int):
        self._send_hardware_command(NameValueTuple(name=HardwareCommandList.ACCELERATE, value=value))

    def _steer(self, value: int):
        self._send_hardware_command(NameValueTuple(name=HardwareCommandList.STEERING, value=value))

    def _stop_motors(self):
        self._send_hardware_command(NameValueTuple(name=HardwareCommandList.STOP_MOVING, value=None))

    def _send_fps_debug(self):
        fps = 1.0/(time() - self._previous_frame_read_time)
        debug = [('AD fps', f'{fps}')]
        self._previous_frame_read_time = time()
        self._send_info(NameValueTuple(name=InfoList.DEBUG, value=debug))

    def _show_image(self, name: str, image: numpy.ndarray):
        self.lock.acquire()
        self._image_queue.put((name, image))
        self.lock.release()


@dataclass
class Parameter:
    name: str
    allowed_values: list
    current_value_index: int

    @property
    def current_value(self):
        return self.allowed_values[self.current_value_index]

    def set_current_value_index(self, value_index):
        if self.is_value_index_valid(value_index):
            self.current_value_index = value_index

    def is_value_index_valid(self, index):
        return 0 <= index < len(self.allowed_values)


class AutonomousDrivingState:
    def __init__(self):
        self.is_active = False
        self.methods_names = []
        self.selected_method_index = 0
        self.selected_method_parameters = []
        self.selected_parameter_index = 0
        self.allowed_values_for_selected_parameter = []

    @property
    def selected_method_name(self):
        return self.methods_names[self.selected_method_index]

    @property
    def selected_method_parameters_names(self) -> list:
        return [p.name for p in self.selected_method_parameters]

    @property
    def selected_parameter_value_index(self) -> any:
        return self.selected_method_parameters[self.selected_parameter_index].current_value_index

    def parameter_value(self, parameter_index):
        if self._is_parameter_index_valid(parameter_index):
            return self.selected_method_parameters[parameter_index].current_value

    def parameter_value_index(self, parameter_index):
        return self.selected_method_parameters[parameter_index].current_value_index

    def select_parameter(self, index):
        if self._is_parameter_index_valid(index):
            self.selected_parameter_index = index

    def _is_parameter_index_valid(self, index: int) -> bool:
        return 0 <= index < len(self.selected_method_parameters)
