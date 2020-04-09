import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


PINS = (11, 13)


def setup():
    """ Set the Raspberry Pi IO configuraton. """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


def teardown():
    GPIO.cleanup()


def _get_pin(target: int):
    assert target < len(PINS)
    return PINS[target]


def pin_constant(target: int, duration: float):
    pin = _get_pin(target)
    GPIO.output(pin, GPIO.HIGH)
    sleep(duration)
    GPIO.output(pin, GPIO.LOW)


def pin_pulse(target: int, reps: int = 1, pulse: float = 0.1):
    # Determine which output pin to use
    pin = _get_pin(target)    
    
    # Pulse
    for _ in range(reps):
        GPIO.output(pin, GPIO.HIGH)
        sleep(pulse)
        GPIO.output(pin, GPIO.LOW)
        sleep(pulse)
