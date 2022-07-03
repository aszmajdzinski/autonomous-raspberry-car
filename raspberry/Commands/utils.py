from Commands.commands import *

user2hardware_commands = {UserCommandList.ACCELERATE: HardwareCommandList.ACCELERATE,
                          UserCommandList.STEERING: HardwareCommandList.STEERING,
                          UserCommandList.STOP_MOVING: HardwareCommandList.STOP_MOVING}

user_commands_for_autonomous_driving = {UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE,
                                        UserCommandList.PREVIOUS,
                                        UserCommandList.NEXT,
                                        UserCommandList.UP,
                                        UserCommandList.DOWN,
                                        UserCommandList.LEFT,
                                        UserCommandList.RIGHT,
                                        UserCommandList.START_STOP_AUTOMOUS_DRIVING}

other_user_commands = {UserCommandList.START_STOP_STATE_RECORDING}


def user2hardware_command(user_command: NameValueTuple) -> NameValueTuple:
    command_name = HardwareCommandList._member_map_[user_command.name.value]
    return NameValueTuple(name=command_name, value=user_command.value)
