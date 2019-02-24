# Project Title

PiHub controlling your Raspberry Pi with WebSockets

### Prerequisites

Python3.7 or higher is required for the Raspberry Pi installation
.net core 2.2  is required for the standalone WebSocket server installation.

### Running PiHub

1. Deploy Python app on your Raspberry following the instructions from the Deployment section
2. Run Raspberry python script using the bash script provided: ./pihub.sh. 
3. Proceed to PiHub WebSocket server  https://puhub.azurewebsites.net or your stand-alone WebSocket server uri.
4. Update connection string with your channel, key and Pi name and click on "Connect" button.

Example of the connection string:
```
wss://pihubdemo.azurewebsites.net/PiHub?channelId=demo&subscriberId=demo&key=demo
```
Also you can use query string parameters to generate connection string from the website URLs as follows:

```
https://pihubdemo.azurewebsites.net/?channel=demo&subscriberId=demo&key=demo
```
5. Click on any command buttons below the command window. Some commands require user input.  Folder contents panel supports interaction with the user. 
6. Click on the "Connect" button to establish websocket connection 

### PiHub commands

* GetFolder - displays raspberry folder in Folder contents panel. Folder panel is interactive. 
Click on a folder opens it. Click on image displays it on image panel. Click on audio file plays it in media player. Click on other file types generates download link.
GetFolder command accept value as folder path. Example: /usr/bin

* GetGPIOPins - return buttons status from your GPIO pins. 0-means unpressed, 1-pressed. The command requires value as a comma-separated list of the GPIO pins to be requested. Example: 1,2,4
* SetGPIOPins - Lighting LEDs (or any other device) using GPIO pins. The command requires value as a comma-separated list of pins and statuses. 0-Led is off, 1- led is on. Example: 1|0,2:1  -means led on pin#0 is off and led on pin 2 is on
* GetFile - Gets the file from the PI. The command requires value containing the path to the file. The image file will be displayed on the image panel. Compatible audio files will be played in on-page media player. Other file types will be available to download by the link above panel.
* PutFile - Puts the file to the PI. The command requires value containing path to the folder for the file to be stored in and file selected in file control.
* GetWebCam - Gets image from the RaspberryPI camera. Requires raspberry camera. 
* ShowInformer - Displays information and plays chimes on attached tv. It tries to switch tv on and take focus(switch on Pi source) if it is possible. Requires value with text memo to be displayed.
* GetAudio - Records audio on Pi and plays it. Requires the value containing the number of seconds to be recorded. Require the microphone to be attached to Pi.
* SwitchOnTv - Switches Tv On if it is attached to the HDMI port. Uses CEC protocol.
* SwitchOffTv- Switches Tv Off if it is attached to the HDMI port. Uses CEC protocol.
* ShowPicture - Displays selected in file control picture on raspberry. Requires tv to be attached to the raspberry.
* PlayAudio - Plays audio file selected by file control. Requires Tv or other audio device attached to Pi.
* RecordAudio - Records audio in the browser and plays it on PI using an audio device attached.

* to be continued. Please contribute to this project to add more commands.

### PiHub events

 PiHubs broadcasts two types of events at the moment:
 * Environment event contains Temperature and Humidity from the Dht11 sensor and system information like CPU, HDD, and RAM usage. Emits every 60 seconds.
 * WebCam event contains an image from the pi camera. Pi emits this event every 60 seconds. 
Use settings in settings.py to adjust this interval.

Disabling these events in pihub.py main function is necessary if there are no appropriate devices attached to the Pi.
 
## Deployment

Copy Python files from the PythonPi folder to your raspberry pi
Install all necessary python modules using PIP
Install audacious on your PI to play audio or update mic.py to use another pi audio player
Update settings.py with your channel name and key. Update gateway base URL if you want to use your one gateway.

Some commands/broadcasts requires microphone, dht11 thermometer, and camera attached to the raspberry PI. If you do not have it, please update the main  function in pihub.py to remove 
initWebcamBroadcast() for the webcam initEnvBroadcast() and for the thermometer.

You can use https://puhub.azurewebsites.net as a hub or deploy standalone WebSocket server.

## Contributing

Please feel free for submitting pull requests to me.

## Author

* **Igor Kanel** - [ikanel](https://github.com/ikanel)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details