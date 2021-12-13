from raspberry.Commands.commands import *
from raspberry.Hardware.arduinoserial import ArduinoCommunication
from queue import Queue
from types import FunctionType
from raspberry.Hardware.motors import MotorControl
from statistics import median


class Hardware(object):
    def __init__(self, config, info_queue: Queue, no_hardware=False):
        self.config = config
        self.info_queue = info_queue
        self.arduino = ArduinoCommunication(config=self.config,
                                            call_when_data_received=self._handle_serial_received_data,
                                            no_hardware=no_hardware)
        self.arduino_command_received: FunctionType
        self.motors = MotorControl(arduino=self.arduino, config=config, info_queue=info_queue)

    def _handle_serial_received_data(self, data: str):
        sonar_data = int(data.split(',')[0])
        self._handle_sonar_data(sonar_data)

    def command(self, command: NameValueTuple):
        if command.name == HardwareCommandList.ACCELERATE:
            self.motors.accelerate(command.value)
        elif command.name == HardwareCommandList.STEERING:
            self.motors.steer(command.value)
        elif command.name == HardwareCommandList.STOP_MOVING:
            self.motors.accelerate(0)

    def _handle_sonar_data(self, value):
        self.info_queue.put(NameValueTuple(name=InfoList.SONAR_VALUE_UPDATED, value=value))

    def shutdown(self):
        self.arduino.close()


class Sonar:
    def __init__(self, iterations):
        self.iterations = iterations
        self.readings = Queue()

    def value(self, v):
        if self.readings.qsize() >= self.iterations:
            self.readings.get()
            self.readings.put(v)
            m = median(list(self.readings.queue))
            return m
        else:
            self.readings.put(v)
            return None
