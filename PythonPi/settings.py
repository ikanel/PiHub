import privatesettings
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

baseUri = f'{privatesettings.gateway}?channelId={privatesettings.channelId}&subscriberId={privatesettings.subscriberId}&key={privatesettings.key}'
