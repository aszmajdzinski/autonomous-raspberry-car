import os

from raspberry.autonomous_driving_manager import AutonomousDrivingState
from raspberry.carstate import CarStateData
from raspberry.utils import get_n_chars


def clear_screen():
    os.system('clear')


class TUI(object):
    def __init__(self, car_state_data: CarStateData):
        self.car_state_data = car_state_data
        self.motor_power_string = ''
        self.steering_value_string = ''
        self.debug = DebugValues(debug_values=self.car_state_data.debug_values)
        self.autonomous_state = AutonomousState(autonomous_mode_enabled=car_state_data.autonomous_mode)

    def print_screen(self):
        clear_screen()
        print(f'Motor power: {self.motor_power_string}\nSteering: {self.steering_value_string}')
        print()
        print(self.debug.get_values_string())
        print()
        print(self.autonomous_state.get_autonomous_state_string())
        print()

    def update_sonar(self):
        pass

    def update_debug_value(self, *args, **kwargs):
        self.debug.update_value(*args, **kwargs)

    def update_motor_power(self):
        self.motor_power_string = str(self.car_state_data.motor_power_value)

    def update_steering_value(self):
        self.steering_value_string = str(self.car_state_data.steering_value)

    def update_autonomous_state_data(self):
        self.autonomous_state.update_data(self.car_state_data.autonomous_mode,
                                          self.car_state_data.autonomous_driving_state)

    def update_all(self):
        self.update_sonar()
        self.update_motor_power()
        self.update_autonomous_state_data()


class DebugValues:
    def __init__(self, debug_values):
        self.debug_values: dict = debug_values

    def update_value(self, key_value):
        for k, v in key_value:
            key = get_n_chars(str(k), 12)
            value = get_n_chars(str(v), 8)
            try:
                self.debug_values[key]
            except KeyError:
                self.debug_values[key] = value
            else:
                if self.debug_values[key] != value:
                    self.debug_values[key] = value

    def get_values_string(self):
        s = ''
        i = 1
        for k, v in self.debug_values.items():
            s = f'{s} {k}: {v} \t'
            if i % 3 == 0:
                s = f'{s}\n'
        return s


class AutonomousState:
    def __init__(self, autonomous_mode_enabled: bool):
        self.autonomous_mode_enabled = autonomous_mode_enabled
        self.autonomous_driving_state: AutonomousDrivingState

    def _mode_string(self) -> str:
        return 'AUTONOMOUS' if self.autonomous_mode_enabled else 'MANUAL'

    def _selected_autonomous_driving_method_string(self) -> str:
        try:
            selected_method_name = \
                self.autonomous_driving_state.methods_names[self.autonomous_driving_state.selected_method_index]
            left_arrow = '<' if self.autonomous_driving_state.selected_method_index > 0 else ' '
            right_arrow = '>' if self.autonomous_driving_state.selected_method_index < \
                                 len(self.autonomous_driving_state.methods_names) - 1 else ' '
            return f'{left_arrow} {selected_method_name} {right_arrow}'
        except AttributeError:
            return ''

    def _parameters_string(self) -> str:
        s = ''
        try:
            selected_parameter_index = self.autonomous_driving_state.selected_parameter_index
            parameters_names = self.autonomous_driving_state.selected_method_parameters_names
            for i, parameter in enumerate(parameters_names):
                parameter_txt = f'   {parameter} ' if i != selected_parameter_index else f'>  {parameter} '
                value_txt = self.autonomous_driving_state.parameter_value(i)
                s = f'{s}{parameter_txt}: {value_txt} \n'
        except AttributeError:
            pass
        return s

    def update_data(self, autonomous_mode_enabled: bool, autonomous_driving_state: AutonomousDrivingState):
        self.autonomous_mode_enabled = autonomous_mode_enabled
        self.autonomous_driving_state = autonomous_driving_state

    def get_autonomous_state_string(self) -> str:
        s = f'Mode: {self._mode_string()}\t'
        if self.autonomous_mode_enabled and self.autonomous_driving_state:
            s = f'{s}Method: {self._selected_autonomous_driving_method_string()}\n {self._parameters_string()} '
        return s
