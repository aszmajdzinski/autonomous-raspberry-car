import pytest
from queue import Queue
from raspberry.Commands.commands import InfoList, HardwareCommandList, NameValueTuple
from raspberry.Hardware.hardware import Hardware


def test_serial_connection_opening(mocker):
    arduino_communication = mocker.patch('raspberry.Hardware.hardware.ArduinoCommunication')
    config = mocker.Mock()

    Hardware(config=config, info_queue=mocker.Mock())

    arduino_communication.assert_called_once_with(config=config,
                                                  call_when_data_received=mocker.ANY,
                                                  no_hardware=mocker.ANY)


def test_serial_connection_not_opening(mocker):
    arduino_communication = mocker.patch('raspberry.Hardware.hardware.ArduinoCommunication')
    config = mocker.Mock()

    Hardware(config=config, info_queue=mocker.Mock(), no_hardware=True)

    arduino_communication.assert_called_once_with(config=config,
                                                  call_when_data_received=mocker.ANY,
                                                  no_hardware=True)


def test_serial_connection_closing(mocker):
    arduino_communication = mocker.patch('raspberry.Hardware.hardware.ArduinoCommunication')
    config = mocker.Mock()

    hardware = Hardware(config=config, info_queue=mocker.Mock())
    hardware.shutdown()

    arduino_communication.return_value.close.assert_called_once()


@pytest.mark.parametrize('value', [-255, -100, 100, 255])
def test_motor_acceleration(value, mocker):
    mocker.patch('raspberry.Hardware.hardware.ArduinoCommunication')
    config = mocker.Mock()
    motors = mocker.patch('raspberry.Hardware.hardware.MotorControl')

    input_command = NameValueTuple(name=HardwareCommandList.ACCELERATE, value=value)

    hardware = Hardware(config=config, info_queue=mocker.Mock(), no_hardware=True)
    hardware.command(command=input_command)

    motors.return_value.accelerate.assert_called_once_with(input_command.value)


@pytest.mark.parametrize('value', [-255, -100, 0, 100, 255])
def test_steering(value, mocker):
    mocker.patch('raspberry.Hardware.hardware.ArduinoCommunication')
    config = mocker.Mock()
    motors = mocker.patch('raspberry.Hardware.hardware.MotorControl')

    input_command = NameValueTuple(name=HardwareCommandList.STEERING, value=value)

    hardware = Hardware(config=config, info_queue=mocker.Mock(), no_hardware=True)
    hardware.command(command=input_command)

    motors.return_value.steer.assert_called_once_with(input_command.value)


@pytest.mark.parametrize('value', [-255, -100, 0, 100, 255])
def test_stop(value, mocker):
    mocker.patch('raspberry.Hardware.hardware.ArduinoCommunication')
    config = mocker.Mock()
    motors = mocker.patch('raspberry.Hardware.hardware.MotorControl')

    input_command = NameValueTuple(name=HardwareCommandList.STOP_MOVING, value=value)

    hardware = Hardware(config=config, info_queue=mocker.Mock(), no_hardware=True)
    hardware.command(command=input_command)

    motors.return_value.accelerate.assert_called_once_with(0)


@pytest.mark.parametrize('value', [0, 10, 255])
def test_receiving_serial_communication(value, mocker):
    arduino_communication = mocker.patch('raspberry.Hardware.hardware.ArduinoCommunication')
    mocker.patch('raspberry.Hardware.hardware.MotorControl')
    info_queue = Queue()

    Hardware(config=mocker.Mock(), info_queue=info_queue)
    arduino_communication.call_args.kwargs["call_when_data_received"](f'{value},')

    assert NameValueTuple(name=InfoList.SONAR_VALUE_UPDATED, value=value) == info_queue.get(block=False)
