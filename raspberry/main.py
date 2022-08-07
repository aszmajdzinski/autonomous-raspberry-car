#!/usr/bin/env python

import signal
from queue import Empty
from threading import Lock
from utils import get_cmd_line_arguments

import utils as utils
from Config.config import Config
from Hardware.hardware import *
from autonomous_driving_manager import AutonomousDrivingManager
from carstate import CarState
from commands_handler import CommandsHandler
from userinterface import UserInterface


class MainApplication:
    def __init__(self, options):
        self.config = Config()
        self.car_state = CarState(config=self.config)
        self.hardware_commands_queue = Queue()
        self.info_queue = Queue()
        self.user_commands_queue = Queue()
        self.image_queue = Queue()
        self.lock = Lock()

        self.hardware = Hardware(config=self.config,
                                 info_queue=self.info_queue,
                                 no_hardware=options.nohardware)

        self.user_interface = UserInterface(self.user_commands_queue,
                                            info_queue=self.info_queue,
                                            car_state=self.car_state,
                                            controller=options.controller,
                                            screen_queue=self.image_queue,
                                            lock=self.lock)

        self.autonomous_driving_manager = AutonomousDrivingManager(hardware_commands_queue=self.hardware_commands_queue,
                                                                   info_queue=self.info_queue,
                                                                   image_queue=self.image_queue,
                                                                   car_state_data_path=options.datapath,
                                                                   lock=self.lock
                                                                   )

        self.car_state.data.autonomous_driving_state = self.autonomous_driving_manager.state

        self.commands_handler = CommandsHandler(car_state=self.car_state, hardware=self.hardware,
                                                info_queue=self.info_queue,
                                                hardware_commands_queue=self.hardware_commands_queue,
                                                user_commands_queue=self.user_commands_queue,
                                                autonomous_driving_manager=self.autonomous_driving_manager,
                                                user_interface=self.user_interface,
                                                shutdown_call=self.shutdown)
        self.enabled = True
        signal.signal(signal.SIGINT, self.shutdown)
        self.start_showing_images()

    def start_showing_images(self):
        while self.enabled:
            try:
                utils.show_image(*self.image_queue.get(block=True, timeout=1))
                self.lock.acquire()
                while not self.image_queue.empty() and self.enabled:
                    utils.show_image(*self.image_queue.get())
                self.lock.release()
            except Empty:
                pass

    def shutdown(self, sig=None, frame=None):
        self.hardware.shutdown()
        self.user_interface.stop()
        self.autonomous_driving_manager.shutdown()
        self.enabled = False
        print("It's now safe to turn off your computer.")


if __name__ == "__main__":
    app = MainApplication(options=get_cmd_line_arguments())
