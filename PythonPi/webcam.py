import time
import datetime
import asyncio
import picamera
import settings

instance = None


def makeWebCamShot(filename, width=640, height=480, warmup=1):
    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        camera.rotation = 90
        time.sleep(warmup)  # Camera warm-up time
        camera.capture(filename)


async def pollWebcam(callback):
    global stopped
    print("Arming webcam polling every {0} seconds".format(settings.webcamBroadcastInterval))
    while settings.enable_webcam_broadcast:
        filename = "PiHubAutoShot.jpg"
        makeWebCamShot(filename, 640, 480)
        await callback(filename)
        await asyncio.sleep(settings.webcamBroadcastInterval)

    print("WebCam Thread cancelled ")


async def test(result):
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)
    else:
        print("error")
