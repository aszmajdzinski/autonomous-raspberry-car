from configparser import ConfigParser


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("Config/config.ini")
        self.load_motor_config()
        self.load_steering_config()
        self.load_communication_config()
        self.load_recording_config()    

    def load_motor_config(self):
        self.motor_minimum_power = self.config['motor'].getint('min_power')
        self.motor_maximum_power = self.config['motor'].getint('max_power')
        self.motor_turbo_power = self.config['motor'].getint('turbo')

    def load_steering_config(self):
        self.steering_servo_range = (self.config['steering'].getint('max_right'),
                                     self.config['steering'].getint('center'),
                                     self.config['steering'].getint('max_left'))

    def load_communication_config(self):
        self.serial_port = self.config['communication']['serial_port']

    def load_recording_config(self):
        self.states_records_dir = self.config['recording']['states_records_dir']
