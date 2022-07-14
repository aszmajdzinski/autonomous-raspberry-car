from AutonomousDrivingMethods.autonomous_driving import AutonomousDrivingAbstractClass, Parameter
from Commands.commands import NameValueTuple, InfoList

import cv2
import numpy as np


class LaneInTheMiddleLinesDetection(AutonomousDrivingAbstractClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Lane In The Middle Lines Detection'
        self.parameters = [Parameter('treshold', (list(range(5, 25, 5))), 2),
                           Parameter('mllength', (list(range(5, 35, 5))), 3),
                           Parameter('mlgap', (list(range(5, 35, 5))), 2),
                           Parameter('oui', ['da', 'tak', 'yes', 'ja'], 1),
                           ]
        self.counter = 0

    def _prepare(self):
        self.counter = 0
        self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('i', self.counter)]))

    def _cleanup(self):

        self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('mode', ' ')]))

    def _process_frame(self):
        img_otsu, img_cropped = self.get_image_otsu(self.frame)
        img_line = self.line_detection(self.frame)
        self._show_image('Camera', self.frame)
        self._show_image('otsu', img_otsu)
        self._show_image('lines', img_line)

    def get_image_otsu(self, img, crop_height=0.8, negative=True, erosion_kernel_size=7, dilation_kernel_size=11):
        img_cropped = img[int(img.shape[0] * crop_height):img.shape[0], 0:img.shape[1]]
        img_cropped_blurred = cv2.GaussianBlur(img_cropped, (5, 5), 0)
        img_cropped_blurred_gray = cv2.cvtColor(img_cropped_blurred, cv2.COLOR_BGR2GRAY)
        _, img_otsu = cv2.threshold(img_cropped_blurred_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img_otsu = cv2.bitwise_not(img_otsu) if negative else img_otsu
        img_otsu_eroded = cv2.erode(img_otsu, np.ones((erosion_kernel_size, erosion_kernel_size), np.uint8))
        return cv2.dilate(img_otsu_eroded, np.ones((dilation_kernel_size, dilation_kernel_size), np.uint8)), \
               img_cropped.copy()

    def line_detection(self, img):
        img_otsu, img_rgb = self.get_image_otsu(img)
        high_threshold = 150
        edges = cv2.Canny(img_otsu, 100, high_threshold)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, None, 20, 20)
        points = []
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
                    cv2.line(img_rgb, (x1, y1), (x2, y2), (255, 0, 0), 5)

        return img_rgb
