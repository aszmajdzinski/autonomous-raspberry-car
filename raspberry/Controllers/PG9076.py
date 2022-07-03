from Commands.commands import GamepadCommands, GamepadEvent, NameValueTuple, UserCommandList
from .controller_parent_class import Controller
from queue import Queue
try:
    from inputs import get_gamepad
except ImportError:
    pass


class GamepadPG9076(Controller):
    def __init__(self, user_command_queue: Queue):
        super().__init__(user_command_queue=user_command_queue)

    def get_user_command(self):
        g = Gamepad().get_event()
        if g is not None:
            return self.handle_gamepad_command(g)

    def handle_gamepad_command(self, command: NameValueTuple) -> NameValueTuple:
        if command.name == GamepadCommands.START:
            return NameValueTuple(name=UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE, value=None)
        elif command.name == GamepadCommands.LB:
            return NameValueTuple(name=UserCommandList.PREVIOUS, value=False)
        elif command.name == GamepadCommands.RB:
            return NameValueTuple(name=UserCommandList.NEXT, value=False)
        elif command.name == GamepadCommands.DPAD_up:
            return NameValueTuple(name=UserCommandList.UP, value=None)
        elif command.name == GamepadCommands.DPAD_down:
            return NameValueTuple(name=UserCommandList.DOWN, value=None)
        elif command.name == GamepadCommands.DPAD_left:
            return NameValueTuple(name=UserCommandList.LEFT, value=None)
        elif command.name == GamepadCommands.DPAD_right:
            return NameValueTuple(name=UserCommandList.RIGHT, value=None)
        elif command.name == GamepadCommands.RT:
            return NameValueTuple(name=UserCommandList.START_STOP_AUTOMOUS_DRIVING, value=None)
        elif command.name == GamepadCommands.LS_v:
            return NameValueTuple(name=UserCommandList.ACCELERATE, value=command.value)
        elif command.name == GamepadCommands.RS_h:
            return NameValueTuple(name=UserCommandList.STEERING, value=command.value)
        elif command.name == GamepadCommands.B:
            return NameValueTuple(name=UserCommandList.START_STOP_STATE_RECORDING, value=None)
        elif command.name == GamepadCommands.HOME:
            return NameValueTuple(name=UserCommandList.SHUTDOWN, value=0)


class Gamepad:
    def __init__(self):
        self._event_types = ['Absolute', 'Key']

    def get_state(self) -> GamepadEvent:
        events = get_gamepad()
        for event in (event for event in events if event.ev_type in self._event_types):
            return GamepadEvent(btn=event.code, value=event.state)

    def get_event(self) -> NameValueTuple:
        gamepad_event = self.get_state()
        if gamepad_event is None: return
        if gamepad_event.btn in ['ABS_Y', 'ABS_Z']:
            return self._handle_analog(gamepad_event)
        elif gamepad_event.btn in ['ABS_HAT0Y', 'ABS_HAT0X']:
            return self._handle_dpad(gamepad_event)
        elif gamepad_event.btn == 'BTN_SOUTH' and gamepad_event.value == 0:
            return NameValueTuple(name=GamepadCommands.Y, value=0)
        elif gamepad_event.btn == 'BTN_MODE' and gamepad_event.value == 1:
            return NameValueTuple(name=GamepadCommands.HOME, value=0)
        elif gamepad_event.btn == 'BTN_TR2' and gamepad_event.value == 0:
            return NameValueTuple(name=GamepadCommands.START, value=0)
        elif gamepad_event.btn == 'BTN_Z' and gamepad_event.value == 0:
            return NameValueTuple(name=GamepadCommands.RB, value=0)
        elif gamepad_event.btn == 'BTN_WEST' and gamepad_event.value == 0:
            return NameValueTuple(name=GamepadCommands.LB, value=0)
        elif gamepad_event.btn == 'BTN_TR' and gamepad_event.value == 0:
            return NameValueTuple(name=GamepadCommands.RT, value=1)
        elif gamepad_event.btn == 'BTN_EAST' and gamepad_event.value == 0:
            return NameValueTuple(name=GamepadCommands.B, value=0)

    def _handle_analog(self, gamepad_event: GamepadEvent) -> NameValueTuple:
        if gamepad_event.btn == 'ABS_Y':
            acc = gamepad_event.value
            return NameValueTuple(name=GamepadCommands.LS_v, value=128 - acc)
        elif gamepad_event.btn == 'ABS_Z':
            acc = gamepad_event.value
            return NameValueTuple(name=GamepadCommands.RS_h, value=128 - acc)

    def _handle_dpad(self, gamepad_event: GamepadEvent) -> NameValueTuple:
        if gamepad_event.btn == 'ABS_HAT0Y':
            if gamepad_event.value == 1:
                return NameValueTuple(GamepadCommands.DPAD_down, 0)
            if gamepad_event.value == -1:
                return NameValueTuple(GamepadCommands.DPAD_up, 0)
            elif gamepad_event.value == 0:
                return NameValueTuple(GamepadCommands.DPAD_v_rel, 0)
        elif gamepad_event.btn == 'ABS_HAT0X':
            if gamepad_event.value == -1:
                return NameValueTuple(GamepadCommands.DPAD_left, 0)
            if gamepad_event.value == 1:
                return NameValueTuple(GamepadCommands.DPAD_right, 0)
            elif gamepad_event.value == 0:
                return NameValueTuple(GamepadCommands.DPAD_h_rel, 0)


if __name__ == "__main__":
    while 1:
        state = Gamepad().get_state()
        if state is not None:
            print(state)
