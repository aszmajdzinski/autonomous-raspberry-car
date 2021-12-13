import os
import time

import cv2

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    pass


class Camera:
    def __init__(self, resolution, framerate=30, rotation=0, car_state_data_path=None):
        self.camera = self.get_simulated_camera_instance(resolution, framerate, rotation, car_state_data_path)\
            if car_state_data_path else self.get_real_camera_instance(resolution, framerate, rotation)

    def get_real_camera_instance(self, resolution, framerate, rotation):
        return RealCamera(resolution, framerate, rotation)

    def get_simulated_camera_instance(self, resolution, framerate, rotation, car_state_data_path):
        return SimulatedCamera(resolution, framerate, rotation, car_state_data_path)

    def initialize_camera(self):
        self.camera.initialize_camera()

    def grab_frame(self):
        return self.camera.grab_frame()


class RealCamera:
    def __init__(self, resolution, framerate=30, rotation=0):
        self.resolution = resolution
        self.framerate = framerate
        self.rotation = rotation
        self.camera = None
        self.rawCapture = None

    def initialize_camera(self):
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.camera.resolution = self.resolution
        self.camera.rotation = self.rotation
        self.camera.framerate = self.framerate
        time.sleep(0.1)

    def grab_frame(self):
        frame = next(self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True))
        self.rawCapture.truncate(0)
        return frame.array


class SimulatedCamera:
    def __init__(self, resolution, framerate=30, rotation=0, car_state_data_path=None):
        self.image_getter = ImageGetter(car_state_data_path)

    def initialize_camera(self):
        pass

    def grab_frame(self):
        return self.image_getter.get_image()


class ImageGetter:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.files = self._get_directory_listing()
        self.current_image_number = 0

    def _get_directory_listing(self):
        files = []
        for (_, _, filenames) in os.walk(self. directory_path):
            files.extend(filenames)
            break
        return sorted(filter(lambda filename: '.png' in filename, files))

    def _get_image(self, filename):
        return cv2.imread(os.path.join(self.directory_path, filename))

    def get_image(self):
        if self.current_image_number < len(self.files):
            filename = self.files[self.current_image_number]
            if self.current_image_number < len(self.files) - 1:
                self.current_image_number += 1
            return self._get_image(filename)

    def get_previous_image(self):
        if self.current_image_number > 0:
            self.current_image_number -= 1
        filename = self.files[self.current_image_number]
        return self._get_image(filename)
