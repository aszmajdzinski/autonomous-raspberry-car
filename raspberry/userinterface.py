from raspberry.carstate import CarState
from raspberry.controller_manager import ControllerManager
from raspberry.text_gui import TUI as TextGUI
from queue import Queue
from time import sleep
from threading import Thread


class UserInterface(object):
    def __init__(self, user_command_queue: Queue, info_queue: Queue, car_state: CarState, controller: str):
        self.user_command_queue = user_command_queue
        self.car_state = car_state
        self.controller = ControllerManager(user_command_queue=self.user_command_queue, controller=controller)
        self.tui = TextGUI(car_state_data=car_state.data)
        self.user_interface_enabled = False
        self.tui_thread = Thread(target=self._tui_worker)
        self.state_updates = {'autonomous_driving': False, 'sonar_value': False, 'motors_power': False,
                              'steering_value': False}
        self._subscribe_to_car_state_updates()
        self.user_interface_enabled = True
        self.controller.start()
        self.tui_thread.start()

    def stop(self):
        self.user_interface_enabled = False
        self.controller.stop()
        self.tui_thread.join()

    def update_debug_data(self, data: list):
        self.tui.update_debug_value(data)

    def autonomous_driving_state_updated(self):
        self.state_updates['autonomous_driving'] = True

    def sonar_value_updated(self):
        self.state_updates['sonar_value'] = True

    def motors_power_updated(self):
        self.state_updates['motors_power'] = True

    def steering_value_updated(self):
        self.state_updates['steering_value'] = True

    def _subscribe_to_car_state_updates(self):
        self.car_state.subscribe_to_autonomous_state_changes(self.autonomous_driving_state_updated)
        self.car_state.subscribe_to_sonars_data_changes(self.sonar_value_updated)
        self.car_state.subscribe_to_motors_power_changes(self.motors_power_updated)
        self.car_state.subscribe_to_steering_value_changes(self.steering_value_updated)

    def _tui_worker(self):
        while self.user_interface_enabled:
            screen_refresh_needed = self.car_state.state_updated or \
                                    self.state_updates['autonomous_driving'] or \
                                    self.state_updates['motors_power'] or \
                                    self.state_updates['steering_value']
            if self.car_state.state_updated:
                self.car_state.state_updated = False

            if self.state_updates['autonomous_driving']:
                self.tui.update_autonomous_state_data()
                self.state_updates['autonomous_driving'] = False

            if self.state_updates['sonar_value']:
                self.tui.update_sonar()
                self.state_updates['sonar_value'] = False

            if self.state_updates['motors_power']:
                self.tui.update_motor_power()
                self.state_updates['motors_power'] = False

            if self.state_updates['steering_value']:
                self.tui.update_steering_value()
                self.state_updates['steering_value'] = False

            if screen_refresh_needed:
                self.tui.print_screen()
            sleep(0.1)
