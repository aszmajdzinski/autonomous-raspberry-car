from threading import Thread


class CollisionAvoidance:
    def __init__(self, info_queue, user_commands_queue, car_state):
        self.collison_avoidance_thread = Thread(target=self._collision_avoidance_worker)
        self.emergency_breaking_thread = Thread(target=self._emergency_breaking_worker())
        self._collision_avoidance_enabled = False
        self._emergency_breaking_enabled = False

    def collision_avoidance(self, enabled):
        self._collision_avoidance_enabled = enabled

    def enable_emergency_breaking(self, enabled):
        self._emergency_breaking_enabled = enabled

    def _collision_avoidance_worker(self):
        while self._collision_avoidance_enabled:
            pass

    def _emergency_breaking_worker(self):
        while self._emergency_breaking_enabled:
            pass
