import RPi.GPIO as GPIO
import time


PIN = 11
VALUE = None


def setValue(value):
    global VALUE
    GPIO.output(PIN, value)
    print("Setting value to:", value)
    VALUE = value

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.OUT)
    setValue(GPIO.LOW)

def toggleValue():
    global VALUE
    value = GPIO.HIGH if (VALUE == GPIO.LOW) else GPIO.LOW
    setValue(value)

def run():
    for _ in range(10):
        toggleValue()
        time.sleep(2)

def main():
    setup()
    run()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
