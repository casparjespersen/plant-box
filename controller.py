import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


PIN = 11


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def listen_for_press(fs: int):
    state = 0
    while True:
        value = bool(GPIO.input(PIN))
        if state:
            if value:
                state += 1
            else:
                yield state/fs
                state = 0
        elif value:
            state = 1
        sleep(1/fs)

def main():
    setup()
    try:
        for duration in listen_for_press(fs=100):
            print("keypress", duration)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()

if __name__ == "__main__":
    main()
