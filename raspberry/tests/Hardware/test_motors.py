from numpy import interp
import pytest
from queue import Queue
from raspberry.Commands.commands import ArduinoCommandList, InfoList, NameValueTuple
from raspberry.Hardware.motors import MotorControl


class Config:
    def __init__(self, motor_minimum_power, motor_maximum_power, steering_servo_range):
        self.motor_minimum_power = motor_minimum_power
        self.motor_maximum_power = motor_maximum_power
        self.steering_servo_range = steering_servo_range


configs = [Config(10, 100, [20, 50, 100]),
           Config(100, 300, [0, 10, 20]),
           Config(50, 100, [55, 90, 120])]  # third case are real hardware parameters


def expected_motor_value(value, config):
    if value == 0:
        return 0
    elif value < 0:
        return -int(interp(abs(value), [0, 127], [config.motor_minimum_power, config.motor_maximum_power]))
    elif value > 0:
        return int(interp(value, [0, 128], [config.motor_minimum_power, config.motor_maximum_power]))


def expected_steer_value(value, config):
    angle = 0
    if value == 0:
        angle = config.steering_servo_range[1]
    elif value < 0:
        angle = interp(value,
                       [-128, 0],
                       [config.steering_servo_range[0], config.steering_servo_range[1]])

    elif value > 0:
        angle = interp(value,
                       [0, 128],
                       [config.steering_servo_range[1], config.steering_servo_range[2]])
    return int(angle)


@pytest.fixture(params=configs)
def get_config(request):
    yield request.param


@pytest.fixture(params=[-127, -50, 50, 128])
def get_accelerate_input_value(request):
    yield request.param


@pytest.fixture(params=[-128, -50, 0, 50, 128])
def get_steering_input_value(request):
    yield request.param


def test_accelerate(get_config, get_accelerate_input_value, mocker):
    arduino = mocker.Mock()
    info_queue = Queue()

    expected_value = expected_motor_value(get_accelerate_input_value, get_config)
    expected_arduino_command = NameValueTuple(name=ArduinoCommandList.MOTOR, value=expected_value)
    expected_info_queue_element = NameValueTuple(name=InfoList.MOTOR_VALUE_UPDATED, value=expected_value)

    motors = MotorControl(arduino=arduino, config=get_config, info_queue=info_queue)
    motors.accelerate(get_accelerate_input_value)

    arduino.send_command.assert_called_once_with(expected_arduino_command)
    assert expected_info_queue_element == info_queue.get(block=False)


def test_stop(get_config, mocker):
    arduino = mocker.Mock()

    info_queue = Queue()

    expected_arduino_command = NameValueTuple(name=ArduinoCommandList.STOP, value=0)
    expected_info_queue_element = NameValueTuple(name=InfoList.MOTOR_VALUE_UPDATED, value=0)

    motors = MotorControl(arduino=arduino, config=get_config, info_queue=info_queue)
    motors.accelerate(0)

    arduino.send_command.assert_called_once_with(expected_arduino_command)
    assert expected_info_queue_element == info_queue.get(block=False)


def test_steering(get_config, get_steering_input_value, mocker):
    arduino = mocker.Mock()
    info_queue = Queue()

    expected_value = expected_steer_value(get_steering_input_value, get_config)
    expected_arduino_command = NameValueTuple(name=ArduinoCommandList.STEERING_SERVO, value=expected_value)
    expected_info_queue_element = NameValueTuple(name=InfoList.STEERING_VALUE_UPDATED, value=expected_value)

    motors = MotorControl(arduino=arduino, config=get_config, info_queue=info_queue)
    motors.steer(get_steering_input_value)

    arduino.send_command.assert_called_once_with(expected_arduino_command)
    assert expected_info_queue_element == info_queue.get(block=False)
