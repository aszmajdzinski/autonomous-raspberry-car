from Controllers import GamepadPG9076, Keyboard
from queue import Queue

try:
    from gamepad import Gamepad
except ImportError:
    pass


class ControllerManager:
    def __init__(self, user_command_queue: Queue, controller='PG9076', info_queue: Queue = None):
        self.user_command_queue = user_command_queue
        self.info_queue = info_queue
        self.controller = self._initialize_controller(controller)

    def start(self):
        self.controller.start()

    def stop(self):
        self.controller.stop()

    def _initialize_controller(self, name: str):
        if name == 'PG9076':
            return GamepadPG9076(user_command_queue=self.user_command_queue)
        elif name == 'keyboard':
            return Keyboard(user_command_queue=self.user_command_queue)
