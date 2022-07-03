import os
import shelve
import sys

import cv2

from datetime import datetime

from carstate import CarStateData
from Config.config import Config
from text_gui import TUI


class CarStateReader:
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self._data_shelve = None
        self.load_data()

    def load_data(self):
        self._data_shelve = shelve.open(self.data_file_path, 'r')

    def show_data(self):
        for key in self._data_shelve.keys():
            print(self._data_shelve[key].motor_power_value)

    def get_timestamps(self):
        return sorted(list(self._data_shelve.keys()))

    def get_entry(self, timestamp: str) -> dict:
        return self._data_shelve[timestamp]


if __name__ == '__main__':

    def get_time_interval(timestamp1: str, timestamp2: str):
        t1 = int(datetime.strptime(timestamps[0], '%Y-%m-%d_%H-%M-%S.%f').timestamp() * 1000)
        t2 = int(datetime.strptime(timestamps[1], '%Y-%m-%d_%H-%M-%S.%f').timestamp() * 1000)
        return t2 - t1
    config = Config()
    path = os.path.join(config.states_records_dir, sys.argv[1])
    car_state_reader = CarStateReader(os.path.join(path, 'car_state_data'))
    timestamps = car_state_reader.get_timestamps()

    car_state = CarStateData(config)
    car_state.load_from_dict(car_state_reader.get_entry(timestamps[0]))
    tui = TUI(car_state_data=car_state)

    for i, timestamp in enumerate(timestamps[:-1]):
        print(timestamp)
        wait = get_time_interval(timestamp, timestamps[i+1])
        car_state.load_from_dict(car_state_reader.get_entry(timestamp))
        tui.car_state_data = car_state
        tui.update_all()
        camera_image = cv2.imread(os.path.join(path, f'{timestamp}.png'))
        cv2.imshow('Camera', camera_image)
        tui.print_screen()
