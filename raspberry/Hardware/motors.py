from raspberry.Hardware.arduinoserial import ArduinoCommunication
from raspberry.Commands.commands import *
from numpy import interp
from queue import Queue


class MotorControl:
    def __init__(self, arduino: ArduinoCommunication, config, info_queue: Queue):
        self.arduino = arduino
        self.config = config
        self.info_queue = info_queue

    def accelerate(self, value: int):
        if value == 0:
            self._control_motor(0)
        elif value < 0:
            self._control_motor(-int(interp(abs(value), [0, 127],
                                            [self.config.motor_minimum_power, self.config.motor_maximum_power])))
        elif value > 0:
            self._control_motor(int(interp(value, [0, 128],
                                           [self.config.motor_minimum_power, self.config.motor_maximum_power])))

    def steer(self, value: int):
        angle = 0
        if value == 0:
            angle = self.config.steering_servo_range[1]
        elif value < 0:
            angle = interp(value,
                           [-128, 0],
                           [self.config.steering_servo_range[0], self.config.steering_servo_range[1]])

        elif value > 0:
            angle = interp(value,
                           [0, 128],
                           [self.config.steering_servo_range[1], self.config.steering_servo_range[2]])
        self._control_servo(int(angle))

    def _control_motor(self, power: int):
        if power:
            self.arduino.send_command(NameValueTuple(ArduinoCommandList.MOTOR, power))
        else:
            self.arduino.send_command(NameValueTuple(ArduinoCommandList.STOP, 0))

        self.info_queue.put(NameValueTuple(name=InfoList.MOTOR_VALUE_UPDATED, value=power))

    def _control_servo(self, value: int):
        self.arduino.send_command(NameValueTuple(name=ArduinoCommandList.STEERING_SERVO, value=value))
        self.info_queue.put(NameValueTuple(name=InfoList.STEERING_VALUE_UPDATED, value=value))
