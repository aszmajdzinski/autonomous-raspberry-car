import numpy as np
from queue import Queue
from threading import Lock


class GUI:
    def __init__(self, screen_image_queue: Queue, lock: Lock):
        self.screen = np.zeros((900, 1600, 3), np.uint8)
        self.screen_image_queue = screen_image_queue
        self.lock = lock

    def refresh_screen(self):
        self.lock.acquire()
        self.screen_image_queue.put(("GUI", self.screen))
        self.lock.release()

    def update_sonar(self):
        pass

    def update_debug_value(self, *args, **kwargs):
        pass

    def update_motor_power(self):
        pass

    def update_steering_value(self):
        pass

    def update_autonomous_state_data(self):
        pass
