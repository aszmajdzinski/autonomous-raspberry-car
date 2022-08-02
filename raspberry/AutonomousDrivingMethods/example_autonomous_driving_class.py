from AutonomousDrivingMethods.autonomous_driving import AutonomousDrivingAbstractClass, Parameter


class ExampleAutonomousDrivingClass(AutonomousDrivingAbstractClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Example Autonomous Driving One'
        self.parameters = [Parameter('a', (list(range(5))), 1),
                           Parameter('b', (list(range(4, 9, 1))), 3),
                           Parameter('txt', ['aaaa', 'bbbb', 'cccc', 'dddd'], 1)]

    def _prepare(self):
        pass

    def _method_cleanup(self):
        pass

    def _process_frame(self):
        pass
