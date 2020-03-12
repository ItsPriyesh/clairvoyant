import pyaudio
import multiprocessing
import wave
import os
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
RECORD_SECONDS = 11
DEVICE_INDEX = 5

def print_available_mics():
    audio = pyaudio.PyAudio()
    #Print out available mics
    for ii in range(audio.get_device_count()):
        print(audio.get_device_info_by_index(ii).get('name'))

def wav_recorder(frames, count, output_buff, audio):
    file_name = str(count)+".wav"
    p_fname = os.path.join('output','raw_audio', file_name)

    waveFile = wave.open(p_fname, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(2)
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    output_buff.put({'file_name': file_name, 'path' : p_fname, 'frames': frames[:]})

def init(input_buff, output_buff):
    print("Initializing Audio Recorder Process...")

    audio = pyaudio.PyAudio()
    
    # Initialize audio stream
    stream = audio.open(
        format=FORMAT, 
        channels=CHANNELS, 
        rate=RATE, 
        input_device_index = DEVICE_INDEX, 
        input=True, 
        frames_per_buffer=CHUNK)

    count = 0

    while(1):
        frames = []
        for i in range(0,int((RATE/CHUNK)*RECORD_SECONDS)):
            frames.append(stream.read(CHUNK))

        #init subprcss
        wav_prcss = multiprocessing.Process(target=wav_recorder, args=(frames[:],count,output_buff,audio,))
        wav_prcss.start()

        count+=1

"""
# stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
stream.close()
p.terminate()    
"""
