from raspberry.AutonomousDrivingMethods.autonomous_driving import AutonomousDrivingAbstractClass, Parameter
from raspberry.Commands.commands import NameValueTuple, InfoList


class AnotherExampleAutonomousDrivingClass(AutonomousDrivingAbstractClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Example Autonomous Driving Two'
        self.parameters = [Parameter('g', (list(range(5))), 0),
                           Parameter('f', (list(range(4, 9, 1))), 4),
                           Parameter('t', ['da', 'ww', 'q', 'vfvf vf'], 1)]
        self.counter = 0

    def _prepare(self):
        self.counter = 0
        self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('i', self.counter)]))

    def _cleanup(self):
        self._stop()
        self._steer(0)
        self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('mode', ' ')]))

    def _process_frame(self):
        self.counter += 1
        self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('i', self.counter)]))
        if 30 < self.counter <= 60:
            self._accelerate(150)
            self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('mode', 'acc')]))
        elif 60 < self.counter <= 90:
            self._steer(100)
            self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('mode', 'steer')]))
        elif self.counter > 110:
            self._stop()
            self._steer(0)
            self._send_info(NameValueTuple(name=InfoList.DEBUG, value=[('mode', 'stop')]))
