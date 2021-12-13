from collections import namedtuple
from enum import Enum

GamepadEvent = namedtuple('GamepadEvent', ['btn', 'value'])
NameValueTuple = namedtuple('NameValue', ['name', 'value'])


class UserCommandList(Enum):
    ACCELERATE = 'ACCELERATE'
    STEERING = 'STEERING'
    STOP_MOVING = 'STOP_MOVING'
    SHUTDOWN = 'SHUTDOWN'
    ENABLE_DISABLE_AUTONOMOUS_MODE = 'ENABLE_AUTONOMOUS_MODE'
    PREVIOUS = 'SELECT_NEXT_AD_METHOD'
    NEXT = 'SELECT_PREVIOUS_AD_METHOD'
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    START_STOP_AUTOMOUS_DRIVING = 'START_AUTONOMOUS_DRIVING'
    START_STOP_STATE_RECORDING = 'START_STOP_STATE_RECORDING'


class ArduinoCommandList(Enum):
    STOP = 'sto'
    MOTOR = 'mot'
    STEERING_SERVO = 'ssr'


class HardwareCommandList(Enum):
    ACCELERATE = 'ACCELERATE'
    STEERING = 'STEERING'
    READ_SONAR = 'READ_SONAR'
    STOP_MOVING = 'STOP_MOVING'


class ArduinoReceivedCommandList(Enum):
    pass


class InfoList(Enum):
    SONAR_VALUE_UPDATED = 'SONARS_DATA_UPDATED'
    MOTOR_VALUE_UPDATED = 'MOTORS_VALUES_UPDATED'
    STEERING_VALUE_UPDATED = 'STEERING_VALUE_UPDATED'
    AUTONOMOUS_DRIVING_STATE_UPDATED = 'AUTONOMOUS_DRIVING_STATE_UPDATED'
    DEBUG = 'DEBUG'
    START_STOP_STATE_RECORDING = 'START_STOP_STATE_RECORDING'
    SAVE_STATE = 'SAVE_STATE'


class GamepadCommands:
    LS_v = 'LEFT_STICK'
    RS_h = 'RIGHT_STICK'
    Y = 'Y'
    B = 'B'
    A = 'A'
    X = 'X'
    DPAD_up = 'DPAD_UP'
    DPAD_down = 'DPAD_DOWN'
    DPAD_v_rel = 'DPAD_VERTICAL_RELEASED'
    DPAD_left = 'DPAD_LEFT'
    DPAD_right = 'DPAD_RIGHT'
    DPAD_h_rel = 'DPAD_HORIZONTAL_RELEASED'
    START = 'START'
    HOME = 'HOME'
    LB = 'LEFT_BUMPER'
    RB = 'RIGHT_BUMPER'
    LT = 'LEFT_TRIGGER'
    RT = 'RIGHT_TRIGGER'



