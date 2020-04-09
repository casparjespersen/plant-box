import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


PIN_IN = 11
PIN_OUT = 13


def setup():
    """ Set the Raspberry Pi IO configuraton. """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_OUT, GPIO.OUT)
    GPIO.output(PIN_OUT, GPIO.LOW)


def listen_for_press(fs: int):
    """ Continuously listen for a button push, and yield the push duration
        after detection. """
    state = 0
    while True:
        value = GPIO.input(PIN_IN)
        if state:
            if value:
                state += 1
            else:
                yield state/fs
                state = 0
        elif value:
            state = 1
        sleep(1/fs)


def show_output(duration: float):
    GPIO.output(PIN_OUT, GPIO.HIGH)
    sleep(duration)
    GPIO.output(PIN_OUT, GPIO.LOW)


def blink(pulse: float, reps: int):
    for _ in range(reps):
        show_output(pulse)
        sleep(pulse)


def main():
    setup()
    try:
        for duration in listen_for_press(fs=100):
            print("Keypress detected.", duration)
            blink(0.1, reps=int(duration)+1)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()


if __name__ == "__main__":
    main()
