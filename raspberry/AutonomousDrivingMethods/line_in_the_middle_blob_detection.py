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
        pos = self._get_current_position()
        if pos is not None:
            steering_value = -cv_utils.get_steer_value_from_image_center(pos, self.frame.shape[1])
            self.steer(steering_value)
        self.show_image('Camera', self.frame)

    def _get_current_position(self):
        cropped_frame = cv_utils.crop_image(self.frame)
        img_otsu = self._get_image_otsu(cropped_frame)
        return self._blob_detection(img_otsu, cropped_frame)

    @staticmethod
    def _get_image_otsu(image):
        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
        gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)
        _, otsu_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        otsu_image = cv2.bitwise_not(otsu_image)
        eroded_image = cv2.erode(src=otsu_image, kernel=np.ones((7, 7)))
        return cv2.dilate(src=eroded_image, kernel=np.ones((11, 11)))

    def _blob_detection(self, bw_image, output_image):
        contour, area = self._get_contour(bw_image)
        if area >= self.parameters[0].current_value:
            center = self._get_center(contour)
            cv2.drawContours(output_image, [contour], 0, (255, 255, 0), 2)
            cv2.circle(output_image, center, 7, (0, 0, 255), -1)
            position = center[0] - output_image.shape[1] / 2
            self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('area', area), ('pos', position)]))
            return int(position)

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
