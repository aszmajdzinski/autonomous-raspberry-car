import numpy as np
from queue import Queue
from threading import Lock
from Gui.drawing import MotorAndSteering, Frame
from typing import Optional


class GUI:
    def __init__(self, screen_image_queue: Queue, lock: Lock):
        self.screen = np.zeros((900, 1600, 3), np.uint8)
        self.screen_image_queue = screen_image_queue
        self.motor_steering = MotorAndSteering(self.screen, position=(1, 502))
        self.lock = lock
        self.draw_basic_screen()
        self.refresh_screen()

    def refresh_screen(self):
        self.lock.acquire()
        self.screen_image_queue.put(("GUI", self.screen))
        self.lock.release()

    def draw_basic_screen(self):
        Frame(screen=self.screen, title="Camera", position=(1, 6), size=(320, 240), fill=(255, 255, 255)).draw()
        Frame(screen=self.screen, title="Preview", position=(330, 6), size=(320, 240)).draw()
        Frame(screen=self.screen, title="Autonomous Driving", position=(1, 254), size=(649, 240)).draw()
        self.motor_steering.draw_basic_window()

    def update_sonar(self, value: Optional[int]):
        pass

    def update_debug_value(self, *args, **kwargs):
        pass

    def update_motor_power(self, value: int):
        self.motor_steering.update_motor_power(value)

    def update_steering_value(self, value: int):
        self.motor_steering.update_steering(value)

    def update_autonomous_state_data(self):
        pass
