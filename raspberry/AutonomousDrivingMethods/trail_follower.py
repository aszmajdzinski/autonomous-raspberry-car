from AutonomousDrivingMethods.autonomous_driving import AutonomousDrivingAbstractClass, Parameter


class TrailFollower(AutonomousDrivingAbstractClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Trail Follower'
        self.parameters = [Parameter('a', (list(range(5))), 1),
                           Parameter('b', (list(range(4, 9, 1))), 3),
                           Parameter('txt', ['aaaa', 'bbbb', 'cccc', 'dddd'], 1)]

        self.image_size = (320, 180)

    def _prepare(self):
        pass

    def _cleanup(self):
        pass

    def _process_frame(self):
        pass
