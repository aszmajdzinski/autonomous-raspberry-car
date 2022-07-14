from AutonomousDrivingMethods.autonomous_driving import AutonomousDrivingAbstractClass, Parameter
from Commands.commands import NameValueTuple, InfoList

import cv2
import numpy as np
from AutonomousDrivingMethods import cv_utils


class LaneInTheMiddleBlobDetection(AutonomousDrivingAbstractClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Lane In The Middle Blob Detection'
        self.parameters = [Parameter('min_area', (list(range(500, 15501, 1000))), 8)]

    def _process_frame(self):
        img_otsu, img_cropped = self._get_image_otsu(self.frame)
        self._blob_detection(img_otsu, img_cropped)
        self._show_image('Camera', self.frame)

    @staticmethod
    def _get_image_otsu(image):
        img_cropped = cv_utils.crop_image(image)
        img_cropped_blurred = cv2.GaussianBlur(img_cropped, (5, 5), 0)
        img_cropped_blurred_gray = cv2.cvtColor(img_cropped_blurred, cv2.COLOR_BGR2GRAY)
        _, img_otsu = cv2.threshold(img_cropped_blurred_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img_otsu = cv2.bitwise_not(img_otsu)
        img_otsu_eroded = cv2.erode(src=img_otsu, kernel=np.ones((7, 7)))
        return cv2.dilate(src=img_otsu_eroded, kernel=np.ones((11, 11))), img_cropped

    def _blob_detection(self, bw_image, color_image):
        contour, area = self._get_contour(bw_image)
        if area >= self.parameters[0].current_value:
            center = self._get_center(contour)
            cv2.drawContours(color_image, [contour], 0, (255, 255, 0), 2)
            cv2.circle(color_image, center, 7, (0, 0, 255), -1)
            self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('area', area)]))

    @staticmethod
    def _get_contour(bw_image):
        contours = cv2.findContours(bw_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        areas = [cv2.contourArea(c) for c in contours]
        max_area_index = areas.index(max(areas))
        return contours[max_area_index], areas[max_area_index]

    @staticmethod
    def _get_center(contour):
        moment = cv2.moments(contour)
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
        return cx, cy
