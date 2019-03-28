# demo
channelId="demo"
subscriberId="pi"
gateway="wss://pihubdemo.azurewebsites.net/PiHub"
key="demo"


# thermometer
thermometer_data_pin = 14

# broadcasting
enable_environment_broadcast = True
environmentBroadcastinterval = 60

enable_webcam_broadcast = True
webcamBroadcastInterval = 60

# microphone
microphone_device_index = 2
microphone_rate = 44100

baseUri = f'{gateway}?channelId={channelId}&subscriberId={subscriberId}&key={key}'
