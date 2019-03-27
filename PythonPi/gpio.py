import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def set_io_pins(pins):
    for pin in pins.split(","):
        pinnum = int(pin.split("|")[0])
        pinval = pin.split("|")[1]
        GPIO.setup(pinnum, GPIO.OUT)

        if (pinval == "0"):
            GPIO.output(pinnum, GPIO.LOW)
            print("pin " + str(pinnum) + " off")
        else:
            GPIO.output(pinnum, GPIO.HIGH)
            print("pin " + str(pinnum) + " on")


def get_io_pins(pins):
    res = []
    for pin in pins.split(","):
        pin_num = int(pin)
        GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        r = pin + "|"
        if GPIO.input(pin_num):
            r += "0"
        else:
            r += "1"
        res.append(r)
    return ",".join(res)
