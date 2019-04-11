#!/usr/bin/env python3.7

import asyncio
import websockets
import json
import base64
import time
import informer
import mic
import webcam
import thermometer as thermo
import sysinfo
import filemanager as fm
import gpio
import os
import settings
import privatesettings
import remotecommand

websocket = None


async def initEnvBroadcast():
    print("initializing environment broadcast")
    if settings.enable_environment_broadcast:
        print("Environment broadcast has started")
        await thermo.pollThermometer(broadcastEnvironmentMessage)


async def initWebcamBroadcast():
    if settings.enable_webcam_broadcast:
        print("Webcam broadcast has started")
        await webcam.pollWebcam(broadcastWebcamMessage)


async def run(uri):
    global websocket
    print("Openning websocket connection to: " + settings.baseUri)
    async with websockets.connect(uri, max_size=1024 * 1024 * 10) as ws:
        websocket = ws
        print("Listening to websocket on " + settings.baseUri)
        while True:
            messageStr = await websocket.recv()
            print("received message")
            message = json.loads(messageStr)
            print(messageStr[0:100])
            output = processIncomingMessage(message)
            if output is not None:
                jsstr = json.dumps(output)
                await websocket.send(jsstr)
                print(jsstr[0:100])
            else:
                print("No response: null output from the inbound message processor")


def prepareBroadcastMessage(name):
    outputMessage = {
        "messageType": "Broadcast",
        "id": time.time(),
        "originator": privatesettings.subscriberId,
        "name": name
    }
    return outputMessage


async def broadcastEnvironmentMessage(result):
    global websocket
    if result.is_valid():
        outputMessage = prepareBroadcastMessage("TemperatureEvent")
        outputMessage["environment"] = {
            "temperature": result.temperature,
            "humidity": result.humidity
        }
        outputMessage["sysInfo"] = {
            "cpu": sysinfo.get_cpu(),
            "ram": sysinfo.get_ram(),
            "temp": sysinfo.get_temp(),
            "disk": sysinfo.get_disk()
        }

        jsstr = json.dumps(outputMessage)
        if websocket != None:
            await websocket.send(jsstr)

        print(jsstr[0:100])


async def broadcastWebcamMessage(filename):
    outputMessage = prepareBroadcastMessage("WebCamEvent")
    outputMessage["blob"] = getBlob(filename)
    jsstr = json.dumps(outputMessage)
    if websocket != None:
        await websocket.send(jsstr)
    print(jsstr[0:100])


def processIncomingMessage(message):
    # print(message)
    outputMessage = None
    name = message["name"]
    messageType= message["messageType"]
    if messageType != "Command":
        return None
    
    value = message["value"]
    intvalue = None
    if value.isdigit():
        intvalue = int(value)

    handlers = {

        "SetGpioPins": [prepareSetGpioPinsResponseMessage],
        "GetGpioPins": [prepareGetGpioPinsResponseMessage],
        "GetFolder": [prepareGetFolderResponseMessage],
        "GetFile": [prepareGetFileResponseMessage],
        "PutFile": [preparePutFileResponseMessage],
        "GetWebCam": [prepareWebCamResponseMessage],
        "ShowInformer": [defaultResponse, informer.showBanner, value],
        "SwitchOnTv": [defaultResponse, informer.switchOnTv],
        "SetWebcamBroadcastInterval": [defaultResponse, setWebcamBroadcastInterval, intvalue],
        "SetEnvironmentBroadcastInterval": [defaultResponse, setEnvironmentBroadcastInterval, intvalue],
        "SwitchOffTv": [defaultResponse, informer.switchOffTv],
        "GetAudio": [prepareAudioMessage],
        "PlayAudio": [playAudioMessage],
        "ShowPicture": [showPicture],
        "RemoteCommand": [executeRemoteCommand]
    }

    try:
        if name not in handlers:
            outputMessage = prepareErrorResponse(message, "Unknown command")
        else:
            command = handlers[name]
            func=command[0]
            outputMessage = func(message, *(command[1:]))

    except OSError as err:
        outputMessage = prepareErrorResponse(message, "OS error: {0}".format(err))

    except RuntimeError as err:
        outputMessage = prepareErrorResponse(message, "OS error: {0}".format(err))

    return outputMessage


def executeRemoteCommand(message):
    if settings.enable_remote_commands:
        outputMessage = prepareDefaultResponse(message)
        cmdresult = remotecommand.execute([message["value"]])
        outputMessage["value"] = cmdresult
        return outputMessage
    else:
        outputMessage = prepareErrorResponse(message, "Remote commands is not enable on this host")
        return outputMessage


def setEnvironmentBroadcastInterval(interval):
    settings.environmentBroadcastinterval = interval


def setWebcamBroadcastInterval(interval):
    settings.webcamBroadcastInterval = interval


def defaultResponse(message, func, *args):
    func(*args)
    outputMessage = prepareDefaultResponse(message)
    return outputMessage


def getBlob(filename):
    blob_read = open(filename, "rb").read()
    blob_64_encode = base64.encodebytes(blob_read).decode("utf-8")
    blob = {
        "name": os.path.basename(filename),
        "size": len(blob_read),
        "content": blob_64_encode
    }
    return blob


def saveFileFromBlob(blob, fileName=None):
    if blob is None:
        return
    if fileName is None:
        fileName = blob["name"]
    f = open(fileName, "wb")
    content = base64.b64decode(blob["content"])
    f.write(content)
    print("the file has been socesfully stored to " + fileName)
    return fileName


def prepareWebCamResponseMessage(message):
    filename = "PiHubShot.jpg"
    webcam.makeWebCamShot(filename)
    outputMessage = prepareDefaultResponse(message)
    outputMessage["blob"] = getBlob(filename)
    return outputMessage


def prepareGetFolderResponseMessage(message):
    outputMessage = prepareDefaultResponse(message)
    location = message["value"]
    outputMessage["directory"] = {"location": location, "files": list(fm.get_folder_content(location))}
    return outputMessage


def prepareGetFileResponseMessage(message):
    outputMessage = prepareDefaultResponse(message)
    filename = message["value"]
    outputMessage["blob"] = getBlob(filename)
    return outputMessage


def preparePutFileResponseMessage(message):
    outputMessage = prepareDefaultResponse(message)
    location = message["value"]
    fullName = location + "/" + message["blob"]["name"]
    print("a file received and will be stored at:" + fullName)
    saveFileFromBlob(message["blob"], fullName)
    return outputMessage


def prepareSetGpioPinsResponseMessage(message):
    outputMessage = prepareDefaultResponse(message)
    pins = message["value"]
    gpio.set_io_pins(pins)
    return outputMessage


def prepareGetGpioPinsResponseMessage(message):
    outputMessage = prepareDefaultResponse(message)
    pins = message["value"]
    outputMessage["gpIoPins"] = gpio.get_io_pins(pins)
    return outputMessage


def prepareAudioMessage(message):
    filename = mic.getAudio(message["value"])
    outputMessage = prepareDefaultResponse(message)
    outputMessage["blob"] = getBlob(filename)
    return outputMessage


def playAudioMessage(message):
    outputMessage = prepareDefaultResponse(message)
    fn = saveFileFromBlob(message["blob"], "audio." + message["blob"]["name"].split(".")[1])
    if fn is None:
        return
    mic.playAudioFile(fn)
    return outputMessage


def showPicture(message):
    outputMessage = prepareDefaultResponse(message)
    fn = saveFileFromBlob(message["blob"], "picture." + message["blob"]["name"].split(".")[1])
    if fn is None:
        return
    informer.showPicture(fn)
    return outputMessage


def prepareErrorResponse(message, error):
    outputMessge = prepareDefaultResponse(message)
    outputMessge["response"]["success"] = "false"
    outputMessge["response"]["responseCode"] = "500"
    outputMessge["response"]["error"] = error
    return outputMessge


def prepareDefaultResponse(message):
    outputMessage = {
        "messageType": "Response",
        "id": time.time(),
        "originator": privatesettings.subscriberId,
        "name": message["name"] + "Response",
        "recipients": [message["originator"]],
        "response":
            {
                "requestId": message["id"],
                "success": "true",
                "responseCode": "200"
            }
    }
    return outputMessage


async def main():
    await asyncio.gather(run(settings.baseUri), initEnvBroadcast(), initWebcamBroadcast())


asyncio.run(main())
