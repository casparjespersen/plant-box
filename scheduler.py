import schedule
import time
from functools import partial
from controller import *

keepalive = partial(pin_pulse, 0, reps=2)
job = partial(pin_pulse, 1, reps=100)


def create_background_scheduler(interval: int = 10):
    scheduler = schedule.Scheduler()
    scheduler.every(interval).seconds.do(keepalive)
    return scheduler


def create_scheduler(interval: int):
    scheduler = schedule.Scheduler()
    scheduler.every(interval).minutes.do(job)
    return scheduler

def run_scheduler(scheduler):
    while True:
        scheduler.run_pending()
        time.sleep(1)
