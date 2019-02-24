#!/usr/bin/env python

import asyncio
import websockets
import json
import logging
import pathlib
import base64
import picamera
import time

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send('''{
                                    recipients:["1","2"],
                                    name:"aaaa",
                                    type:"Command",
                                    id:"7272727"
                            ''')

message='{recipients:["1","2"],name:"aaaa",type:"Command",id:"python7272727"}'
baseUri='ws://localhost:12125/PiHub?channelId=1&subscriberId=3'

async def run(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            messageStr = await websocket.recv()
            message=json.loads(messageStr)
            output=processIncomingMessage(message)
            if output is not None:
                jsstr=json.dumps(output)
                await websocket.send(jsstr)
         


def processIncomingMessage(message):
    outputMessage=None
    if message["name"]=="GetWebCam":
        outputMessage=prepareWebCamMessage(message)
    return outputMessage


def getBlob(filename):
    blob_read=open(filename, "rb").read()
    blob_64_encode = base64.encodestring(blob_read).decode("utf-8") 
    blob= {
            "name":filename,
            "size":len(blob_read),
            "content":blob_64_encode
           }
    return blob

def makeWebCamShot(filaname):
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        time.sleep(10) # Camera warm-up time
        camera.capture(filename)

def prepareWebCamMessage(message):
    filename="PiHubShot.jpg"
    makeWebCamShot(filaname)
    outputMessage= {
            "messageType":"Response",
            "id":"1",
            "originator":"3",
            "name":"WebCamResponse",
            "recipients":[message["originator"]],
            "response":
                    {
                        "requestId":message["id"],
                        "success":"true",
                        "responseCode":"200"
                    },
            "blob":getBlob(filename)
            
        }
    return outputMessage

asyncio.get_event_loop().run_until_complete(run(baseUri))



