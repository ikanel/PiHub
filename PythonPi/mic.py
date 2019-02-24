import pyaudio
import wave
import os
import audioop

def getAudio(record_secs):
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'sound.wav' # name of .wav file

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*int(record_secs))):
        data = stream.read(chunk, exception_on_overflow = False)
        frames.append(data)

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    converted = audioop.ratecv(b''.join(frames), 2, chans, samp_rate, 11025, None)
    #converted = audioop.lin2lin(converted[0], 2, 1)
    #converted = audioop.bias(converted, 1, 128)

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(11025)
    wavefile.writeframes(converted[0])
    wavefile.close()

    return wav_output_filename

def playAudioFile(filename):
    playerCommandLineString="audacious -H -q -p {0}"
    os.system(playerCommandLineString.format(filename))
    

def playWav(filename):
    
    #define stream chunk   
    chunk = 1024  

    #open a wav format music  
    f = wave.open(filename,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream
    #print(f.getsampwidth(),f.getnchannels(),f.getframerate())
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

#playWav(getAudio(5))
#playAudioFile("audio.wav")
