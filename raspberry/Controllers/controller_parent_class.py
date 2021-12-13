from abc import ABC, abstractmethod
from threading import Thread
from queue import Queue


class Controller(ABC):
    def __init__(self, user_command_queue: Queue):
        self.user_command_queue = user_command_queue
        self.worker = Thread(target=self._worker, daemon=True)
        self.worker.start()
        self.user_commands_count = 0

    def start(self):
        pass

    def stop(self):
        pass

    @abstractmethod
    def get_user_command(self):
        pass

    def _worker(self):
        while True:
            user_command = self.get_user_command()
            if user_command:
                self.user_command_queue.put(user_command)
