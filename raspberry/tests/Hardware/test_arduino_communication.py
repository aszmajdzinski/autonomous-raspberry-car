import pytest
from raspberry.Commands.commands import ArduinoCommandList, NameValueTuple
from raspberry.Hardware.arduinoserial import ArduinoCommunication


def test_open_connection_with_hardware(mocker):
    arduino_serial = mocker.patch("raspberry.Hardware.arduinoserial.ArduinoSerial")

    ArduinoCommunication(config=mocker.Mock(), call_when_data_received=mocker.Mock(), no_hardware=False)

    arduino_serial.return_value.read_thread.start.assert_called_once()


def test_not_open_connection_without_hardware(mocker):
    arduino_serial = mocker.patch("raspberry.Hardware.arduinoserial.ArduinoSerial")

    ArduinoCommunication(config=mocker.Mock(), call_when_data_received=mocker.Mock(), no_hardware=True)

    arduino_serial.return_value.read_thread.start.assert_not_called()


def test_used_config_and_call(mocker):
    arduino_serial = mocker.patch("raspberry.Hardware.arduinoserial.ArduinoSerial")
    config = mocker.Mock()
    call = mocker.Mock()
    ArduinoCommunication(config=config, call_when_data_received=call)

    arduino_serial.assert_called_once_with(config=config, call_when_data_received=call)


@pytest.mark.parametrize('command_name, value',
                         [(ArduinoCommandList.MOTOR, 10),
                          (ArduinoCommandList.STEERING_SERVO, 5)])
def test_serial_write(command_name, value, mocker):
    arduino_serial = mocker.patch("raspberry.Hardware.arduinoserial.ArduinoSerial")

    expected_value = f'{command_name.value}{value}'

    arduino_communication = ArduinoCommunication(config=mocker.Mock(), call_when_data_received=mocker.Mock())
    arduino_communication.send_command(NameValueTuple(name=command_name, value=value))

    arduino_serial.return_value.write.assert_called_once_with(expected_value)


def test_close(mocker):
    arduino_serial = mocker.patch("raspberry.Hardware.arduinoserial.ArduinoSerial")

    arduino_communication = ArduinoCommunication(config=mocker.Mock(), call_when_data_received=mocker.Mock())
    arduino_communication.close()

    arduino_serial.return_value.stop_reading.assert_called_once()
