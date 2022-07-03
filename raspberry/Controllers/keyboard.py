from Commands.commands import GamepadCommands, NameValueTuple, UserCommandList
from .controller_parent_class import Controller
from pynput import keyboard
from queue import Queue


class Keyboard(Controller):
    def __init__(self, user_command_queue: Queue):
        self.keys = Queue()
        super().__init__(user_command_queue=user_command_queue)
        self.keyboard_listener = keyboard.Listener(on_press=self._key_pressed,
                                                   on_release=self._key_released,
                                                   suppress=True)

    def start(self):
        self.keyboard_listener.start()

    def stop(self):
        self.keyboard_listener.stop()

    def get_user_command(self):
        return self._handle_key(self.keys.get(block=True))

    def _key_pressed(self, key):
        self.keys.put((key, 'pressed'))

    def _key_released(self, key):
        self.keys.put((key, 'released'))

    def _handle_key(self, key):
        key_string = str(key[0])
        event = key[1]

        if event == 'released':
            if key_string in ('Key.up', 'Key.down'):
                return NameValueTuple(name=UserCommandList.ACCELERATE, value=0)
            elif key_string in ('Key.left', 'Key.right'):
                return NameValueTuple(name=UserCommandList.STEERING, value=0)

        if event == 'pressed':
            if key_string == 'Key.space':
                return NameValueTuple(name=UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE, value=None)
            elif key_string == '\',\'':
                return NameValueTuple(name=UserCommandList.PREVIOUS, value=False)
            elif key_string == '\'.\'':
                return NameValueTuple(name=UserCommandList.NEXT, value=False)
            elif key_string == 'Key.page_up':
                return NameValueTuple(name=UserCommandList.UP, value=None)
            elif key_string == 'Key.page_down':
                return NameValueTuple(name=UserCommandList.DOWN, value=None)
            elif key_string == '\'-\'':
                return NameValueTuple(name=UserCommandList.LEFT, value=None)
            elif key_string == '\'=\'':
                return NameValueTuple(name=UserCommandList.RIGHT, value=None)
            elif key_string == 'Key.enter':
                return NameValueTuple(name=UserCommandList.START_STOP_AUTOMOUS_DRIVING, value=None)
            elif key_string == 'Key.up':
                return NameValueTuple(name=UserCommandList.ACCELERATE, value=128)
            elif key_string == 'Key.down':
                return NameValueTuple(name=UserCommandList.ACCELERATE, value=-127)
            elif key_string == 'Key.left':
                return NameValueTuple(name=UserCommandList.STEERING, value=128)
            elif key_string == 'Key.right':
                return NameValueTuple(name=UserCommandList.STEERING, value=-127)
            elif key_string == 'Key.tab':
                return NameValueTuple(name=UserCommandList.START_STOP_STATE_RECORDING, value=None)
            if key_string == 'Key.esc':
                return NameValueTuple(name=UserCommandList.SHUTDOWN, value=0)
            else:
                return None
