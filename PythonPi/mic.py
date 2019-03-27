import pyaudio
import wave
import math
import os
import audioop
import settings


def getAudio(record_secs):
    form_1 = pyaudio.paInt16  # 16-bit resolution
    chans = 1  # 1 channel
    samp_rate = settings.microphone_rate  # 44.1kHz sampling rate
    chunk = 512  # chunk size above 512 causes oerflow in the buffer
    dev_index = settings.microphone_device_index  # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'sound.wav'  # name of .wav file

    audio = pyaudio.PyAudio()  # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format=form_1, rate=samp_rate, channels=chans, \
                        input_device_index=dev_index, input=True, \
                        frames_per_buffer=chunk)
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0, int(math.ceil(samp_rate / chunk) * int(record_secs))):
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    converted = audioop.ratecv(b''.join(frames), 2, chans, samp_rate, 8000, None)

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename, 'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(8000)
    wavefile.writeframes(converted[0])
    # wavefile.writeframes(b''.join(frames))
    wavefile.close()

    return wav_output_filename


def playAudioFile(filename):
    playerCommandLineString = "audacious -H -q -p {0}"
    os.system(playerCommandLineString.format(filename))


def playWav(filename):
    # define stream chunk
    chunk = 1024

    # open a wav format music
    f = wave.open(filename, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    # print(f.getsampwidth(),f.getnchannels(),f.getframerate())
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

        # stop stream
    stream.stop_stream()
    stream.close()
