import cv2
import numpy as np
from Gui.colors import Colors
from numpy import interp


class MotorAndSteering:
    def __init__(self, screen: np.ndarray, position: tuple[int, int]):
        self.x, self.y = position
        self.screen = screen

    def draw_basic_window(self):
        Frame(screen=self.screen, title="Move", position=(self.x, self.y), size=(320, 240)).draw()
        cv2.putText(self.screen, 'Power', (self.x + 13, self.y + 28), cv2.FONT_HERSHEY_PLAIN, 1.1, Colors.YELLOW)
        cv2.putText(self.screen, 'Steering', (self.x + 13, self.y + 50), cv2.FONT_HERSHEY_PLAIN, 1.1, Colors.YELLOW)
        self._draw_motor_value_text(0)
        self._draw_motor_value_bar(0)
        self._draw_steering_value_text(0)
        self._draw_steering_value_bar(0)

    def update_motor_power(self, value: int):
        self._draw_motor_value_text(value)
        self._draw_motor_value_bar(value)

    def update_steering(self, value: int):
        self._draw_steering_value_text(value)
        self._draw_steering_value_bar(value)

    def _draw_motor_value_text(self, value: int):
        pt1 = (self.x + 265, self.y + 14)
        pt2 = (pt1[0] + 45, pt1[1] + 15)
        cv2.rectangle(self.screen, pt1, pt2, Colors.BLACK, -1)
        cv2.putText(self.screen, str(value), (pt1[0], pt2[1]), cv2.FONT_HERSHEY_PLAIN, 1, Colors.WHITE)

    def _draw_motor_value_bar(self, value):
        max_width, height = 150, 12
        x_shift, y_shift = 105, 17
        pt1_black, pt2_black = (self.x + x_shift, self.y + y_shift), (self.x + x_shift + max_width, self.y + y_shift + height)
        cv2.rectangle(self.screen, pt1_black, pt2_black, Colors.BLACK, -1)
        pt1_red = (self.x + x_shift + max_width // 2, self.y + y_shift)
        width = int(interp(value, [-255, 255], [-max_width//2, max_width//2]))
        pt2_red = (pt1_red[0] + width, pt1_red[1] + height)
        cv2.rectangle(self.screen, pt1_red, pt2_red, Colors.DARK_RED, -1)

    def _draw_steering_value_text(self, value: int):
        x_shift, y_shift = 265, 35
        pt1 = (self.x + x_shift, self.y + y_shift)
        pt2 = (pt1[0] + 45, pt1[1] + 15)
        cv2.rectangle(self.screen, pt1, pt2, Colors.BLACK, -1)
        cv2.putText(self.screen, str(value), (pt1[0], pt2[1]), cv2.FONT_HERSHEY_PLAIN, 1, Colors.WHITE)

    def _draw_steering_value_bar(self, value):
        max_width, height = 150, 12
        x_shift, y_shift = 105, 40
        pt1_black, pt2_black = (self.x + x_shift, self.y + y_shift), (self.x + x_shift + max_width, self.y + y_shift + height)
        cv2.rectangle(self.screen, pt1_black, pt2_black, Colors.BLACK, -1)
        pt1 = (self.x + x_shift + max_width // 2, self.y + y_shift)
        width = int(interp(value, [-255, 255], [-max_width // 2, max_width // 2]))
        pt2 = (pt1[0] + width, pt1[1] + height)
        cv2.rectangle(self.screen, pt1, pt2, Colors.DARK_RED, -1)


class Frame:
    def __init__(self, screen, title, position: tuple[int, int], size: tuple[int, int], fill=None):
        self.screen = screen
        self.title = title
        self.x, self.y = position
        self.width, self.height = size[0], size[1]
        self.thickness = 2
        self.fill = fill

    def draw(self):
        cv2.line(self.screen, (self.x, self.y), (self.x, self.y + self.height), Colors.GREEN, self.thickness)
        cv2.line(self.screen, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height),
                 Colors.GREEN, self.thickness)
        cv2.line(self.screen, (self.x + self.width, self.y + self.height), (self.x + self.width, self.y),
                 Colors.GREEN, self.thickness)
        cv2.line(self.screen, (self.x + self.width, self.y), (self.x + 77, self.y), Colors.GREEN,
                 self.thickness)
        cv2.line(self.screen, (self.x, self.y), (self.x + 20, self.y), Colors.GREEN, self.thickness)
        cv2.putText(self.screen, self.title, (self.x + 22, self.y + 7), cv2.FONT_HERSHEY_PLAIN, 1.4, Colors.WHITE)
