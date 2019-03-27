import dht11
import RPi.GPIO as GPIO
import settings
import datetime
import asyncio

instance = None


def initialize(pin=14):
    global instance
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # read data using pin 14
    instance = dht11.DHT11(pin)
    return instance


def getValue():
    result = instance.read()
    if (result.is_valid() == True):
        return result
    else:
        return None


async def pollThermometer(timeout, callback):
    global stopped
    print("Arming thermometer polling every {0} seconds".format(timeout))
    while settings.enable_environment_broadcast:

        result = getValue()
        print("result {0}".format(result))

        if result != None:
            await callback(result)
        else:
            print("Cannot read thermometer")

        if timeout > 0:
            await asyncio.sleep(timeout)


async def test(result):
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)
    else:
        print("error")


initialize(settings.thermometer_data_pin)
