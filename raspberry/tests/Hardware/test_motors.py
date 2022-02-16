from numpy import interp
import pytest
from queue import Queue
from raspberry.Commands.commands import ArduinoCommandList, InfoList, NameValueTuple
from raspberry.Hardware.motors import MotorControl
from unittest.mock import Mock


class Config:
    def __init__(self):
        self.motor_minimum_power = 0
        self.motor_maximum_power = 100
        self.steering_servo_range = [10, 20, 50]


def test_accelerate():
    config = Config()
    arduino = Mock()
    info_queue = Queue()

    input_value = 10

    expected_value = int(interp(input_value, [0, 128], [config.motor_minimum_power, config.motor_maximum_power]))
    expected_arduino_command = NameValueTuple(name=ArduinoCommandList.MOTOR,
                                              value=expected_value)
    expected_info_queue_element = NameValueTuple(name=InfoList.MOTOR_VALUE_UPDATED, value=expected_value)

    motors = MotorControl(arduino=arduino, config=config, info_queue=info_queue)
    motors.accelerate(input_value)

    arduino.send_command.assert_called_once_with(expected_arduino_command)
    assert expected_info_queue_element == info_queue.get()
