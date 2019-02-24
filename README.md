# Project Title

PiHub controlling your Raspberry Pi with websockets

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python3.7 or higher is required for the Rapberry Pi installation
.net core 2.2  is required for the standalone websocket server installation.

### Running PiHub

1. Deploy Python app on your Raspberry following the instructions from the Deployment section
2. Run Raspberry python using bash script provided: ./pihub.sh. 
3. Proceed to PiHub websocket server url - https://puhub.azurewebsites.net or your stand-alone installation url
4. Update connection string with your channel, key and Pi name. 
5. Click on any command buttons below the command window. Some commands requres user input.  Folder contents panel supports user interaction. 

Example:
```
wss://pihubdemo.azurewebsites.net/PiHub?channelId=demo&subscriberId=demo&key=demo
```
or you can use querystring parameters to generate connection string from the website urls as follows:

```
https://pihubdemo.azurewebsites.net/?channel=demo&subscriberId=demo&key=demo
```

6. Click on "Connect" button to establish websocket connection 



### PiHub commads

* GetFolder - displays raspberry folder in Folder contents panel.Folder panel is interactive. 
Click on folder opens it. Click on image displays it on image panel.
Click on audio file plays it in media player. Click on other file types genarates download link.
Getfoler command accept value as folder path. Exemple: /usr/bin

* GetGPIOPins - return buttons status from your GPIO pins. 0-means unpressed, 1-pressed. The command requres value as a comma separated list of the GPIO pins to be requested. Example: 1,2,4
* SetGPIOPins - Lighting leds (or any other device) using GPIO pins. The command requers value as a comma-separated list of pins and statuses. 0-Led is off, 1- led is on. Example: 1|0,2:1  -means led on pin#0 is off and led on pin 2 is on
* GetFile - Gets file from the PI. The commands requires value contining path to the file. Image file will be dispalyed on image panel. Compatimble audio files will be played in media player. Other file types will by available to download by the link above panel.
* PutFile - Puts file to the PI.The commands requires value contining path to the folder for the file to be stored in and file selected in file control.
* GetWebCam - Gets image from the RaspberryPI camera. Requires raspberry camera. 
* ShowInformer - Displays information and plays chimes on attached tv. It tries to swicth tv on and take focus(switch on Pi source) if it possible. Reqires value with  text memo to be dispayed.
* GetAudio - Records audio on Pi and plays it. Requres the value containing number of seconds to be recorder. Require microphone to be attached to Pi.
* SwitchOnTv - Switches Tv On if it is attached to the hdmi port. Uses CEC protocol.
* SwitchOffTv- Switches Tv Off if it is attached to the hdmi port. Uses CEC protocol.
* ShowPicture - Displays selected in file control picture on raspberry. Requires tv to be attached to the raspberry.
* PlayAudio - Plays audio file selected by file control. Requres Tv or other audio device attached to Pi.
* RecordAudio - Records audio in browser and plays it on PI using audio device attached.

* to be continued. Please contribute to this project to add more commands.

### PiHub events

 PiHubs broadcasts two type of events at the moment:
 * Environment event contains Themperature and Humidity from the Dht11 sensor and system information like CPU,HDD and RAM usage. Emits every 60 seconds.
 * WebCam event contains image from the WebCamera. Pi emits this event every 60 secons. Use settings to adjust this interval.

 Please disable these events in pihub.py main function if you do not have appropriate devices attached to the Pi.
 
## Deployment

Copy Python files from the PythonPi folder to your raspberry pi
Install all nessesary python modules using PIP
Install audacious on your PI to play audio or update mic.py to use another pi audio player
Update settings.py with your channel name and key. Update gateway base url if you want to use your one gateway.

Some commands/broadcasts requres microphone, dht11 thermometer and camera attached to the raspberry PI. If you do not have it please update main  function in pihub.py to remove 
initWebcamBroadcast() for the webcam initEnvBroadcast() and for the thermometer.

You can use https://puhub.azurewebsites.net as a hub or deploy standalone websocket server.

## Contributing

Please feel free for submitting pull requests to me.

## Author

* **Igor Kanel** - [ikanel](https://github.com/ikanel)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details