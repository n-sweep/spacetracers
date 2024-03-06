import os
import requests
import threading
from time import sleep
from queue import Queue


class RateLimiter:
    q = Queue()
    results = {}
    started = False

    def __init__(self, limit=1):
        self.limit = limit
        self.start()

    def process_request(self, event, args, kwargs):
        # process the request
        print(args, kwargs)
        result = requests.request(*args, **kwargs)

        # put the results of the request into the results dict
        self.results[event] = result

        # notify that the request is processed
        event.set()

    def worker(self):
        while self.started:
            # retrieve an event from the queue
            event, args, kwargs = self.q.get()

            # process the event & sleep to control the rate of requests
            self.process_request(event, args, kwargs)
            sleep(self.limit)

    def queue_request(self, args, kwargs):
        # make an event for tracking completion of the request
        event = threading.Event()

        # add the request to the queue and wait for completion
        self.q.put((event, args, kwargs))
        event.wait()

        # return the result
        result = self.results.pop(event)
        return result

    def start(self):
        self.started = True
        t = threading.Thread(target=self.worker, daemon=True)
        t.start()

    def stop(self):
        self.started = False


def ensure_directory(dir):
    """ ensure the directory exists """
    if os.path.isfile(dir):
        dir = os.path.dirname(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
