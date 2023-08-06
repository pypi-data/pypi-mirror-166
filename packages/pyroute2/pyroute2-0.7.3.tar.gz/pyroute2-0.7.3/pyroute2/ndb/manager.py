import queue


class TaskRouter:

    def __init__(self, maxsize=None):
        self.queue = queue.Queue(maxsize=maxsize)
        self.routing = {}

    @classmethod
    def publish(cls, key, route):
        self.routing[key] = route

    def __next__(self):
        return self.queue.get()

    def __iter__(self):
        return self
