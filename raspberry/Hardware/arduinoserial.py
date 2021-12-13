from raspberry.Commands.commands import NameValueTuple
from raspberry.Config.config import Config
from threading import Thread

try:
    import serial
except:
    pass


class ArduinoSerial:
    def __init__(self, config: Config, call_when_data_received: callable):
        self._connection = serial.Serial(
            port=config.serial_port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.call_when_data_received = call_when_data_received
        self.read_enabled = True
        self.read_thread = Thread(target=self._read_worker)

    def write(self, text):
        if text is not None:
            self._connection.write(str.encode(text + '\n'))

    def _read_worker(self):
        while self.read_enabled:
            received_data = self._connection.readline().rstrip()
            if received_data:
                self.call_when_data_received(received_data.decode())

    def stop_reading(self):
        self.read_enabled = False
        self.read_thread.join(timeout=1)
        self._connection.close()


class ArduinoCommunication:
    def __init__(self, config, call_when_data_received: callable, no_hardware=False):
        self.config = config
        self.serial = None
        self.function_to_call_when_data_received = call_when_data_received
        self.no_hardware = no_hardware
        if not self.no_hardware:
            self._open_serial_connection()

    def send_command(self, command: NameValueTuple):
        if not self.no_hardware:
            serial_command = self._create_command_string(command)
            self.serial.write(serial_command)

    def _open_serial_connection(self):
        self.serial = ArduinoSerial(config=self.config, call_when_data_received=self.function_to_call_when_data_received)
        self.serial.read_thread.start()

    def _create_command_string(self, command: NameValueTuple):
        return '{}{}'.format(command.name.value, command.value)

    def close(self):
        if not self.no_hardware:
            self.serial.stop_reading()
