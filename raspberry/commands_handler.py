from raspberry.carstate import CarState
from raspberry.Hardware.hardware import *
from queue import Queue
from raspberry.Commands.commands import InfoList, UserCommandList
from raspberry.userinterface import UserInterface
import raspberry.Commands.command_utils as main_utils
from raspberry.autonomous_driving_manager import AutonomousDrivingManager
from threading import Thread


class CommandsHandler:
    def __init__(self, car_state: CarState, hardware: Hardware, info_queue: Queue, hardware_commands_queue: Queue,
                 user_commands_queue: Queue, autonomous_driving_manager: AutonomousDrivingManager,
                 user_interface: UserInterface, shutdown_call: callable):
        self.car_state = car_state
        self.hardware = hardware
        self.info_queue = info_queue
        self.hardware_commands_queue = hardware_commands_queue
        self.user_commands_queue = user_commands_queue
        self.autonomous_driving_manager = autonomous_driving_manager
        self.user_interface = user_interface
        self._hardware_commands_thread = Thread(target=self._hardware_commands_worker, daemon=True)
        self._info_worker = Thread(target=self._info_queue_worker, daemon=True)
        self._user_commands_thread = Thread(target=self._user_commands_worker, daemon=True)
        self.shutdown = shutdown_call
        self._hardware_commands_thread.start()
        self._info_worker.start()
        self._user_commands_thread.start()

    def _info_queue_worker(self):
        while True:
            info = self.info_queue.get(block=True)
            if info.name == InfoList.DEBUG:
                self.user_interface.update_debug_data(info.value)
            else:
                self.car_state.update_state(info)

    def _hardware_commands_worker(self):
        while True:
            self.hardware.command(self.hardware_commands_queue.get(block=True))

    def _user_commands_worker(self):
        while True:
            command = self.user_commands_queue.get(block=True)
            if command.name == UserCommandList.SHUTDOWN:
                self.shutdown()
                return

            if self.car_state.data.autonomous_mode:
                self._handle_user_command_in_autonomous_mode(command)
            else:
                self._handle_user_command_in_manual_mode(command)

    def _handle_user_command_in_autonomous_mode(self, command: NameValueTuple):
        if command.name == UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE:
            self._handle_autonomous_driving_command(
                NameValueTuple(name=UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE, value=False))
        elif command.name in main_utils.user2hardware_commands.keys():
            self._handle_hardware_command(command)
        elif command.name in main_utils.user_commands_for_autonomous_driving:
            self._handle_autonomous_driving_command(command)
        elif command.name == UserCommandList.START_STOP_STATE_RECORDING:
            self.car_state.update_state(NameValueTuple(InfoList.START_STOP_STATE_RECORDING, None))

    def _handle_user_command_in_manual_mode(self, command: NameValueTuple):
        if command.name == UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE:
            self._handle_autonomous_driving_command(
                NameValueTuple(name=UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE, value=True))
        elif command.name in main_utils.user2hardware_commands.keys():
            self._handle_hardware_command(command)
        elif command.name == GamepadCommands.START:
            return NameValueTuple(name=UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE, value=True)

    def _handle_hardware_command(self, cmd):
        self.hardware_commands_queue.put(main_utils.user2hardware_command(cmd))

    def _handle_autonomous_driving_command(self, cmd: NameValueTuple):
        selected_method_index = self.autonomous_driving_manager.state.selected_method_index
        selected_parameter_index = self.autonomous_driving_manager.state.selected_parameter_index
        selected_parameter_value_index = self.autonomous_driving_manager.state.selected_parameter_value_index

        if cmd.name == UserCommandList.ENABLE_DISABLE_AUTONOMOUS_MODE:
            if not cmd.value:
                self.autonomous_driving_manager.stop()
            self.car_state.data.autonomous_mode = cmd.value

        elif cmd.name == UserCommandList.PREVIOUS:
            self.autonomous_driving_manager.select_method(selected_method_index - 1)

        elif cmd.name == UserCommandList.NEXT:
            self.autonomous_driving_manager.select_method(selected_method_index + 1)

        elif cmd.name == UserCommandList.UP:
            self.autonomous_driving_manager.select_parameter(selected_parameter_index - 1)

        elif cmd.name == UserCommandList.DOWN:
            self.autonomous_driving_manager.select_parameter(selected_parameter_index + 1)

        elif cmd.name == UserCommandList.LEFT:
            self.autonomous_driving_manager.select_parameter_value_index(selected_parameter_index,
                                                                         selected_parameter_value_index - 1)

        elif cmd.name == UserCommandList.RIGHT:
            self.autonomous_driving_manager.select_parameter_value_index(selected_parameter_index,
                                                                         selected_parameter_value_index + 1)

        elif cmd.name == UserCommandList.START_STOP_AUTOMOUS_DRIVING:
            if not self.autonomous_driving_manager.state.is_active:
                self.autonomous_driving_manager.start()
            else:
                self.autonomous_driving_manager.stop()

        self.info_queue.put(NameValueTuple(InfoList.AUTONOMOUS_DRIVING_STATE_UPDATED, None))
