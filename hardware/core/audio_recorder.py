import pyaudio
import multiprocessing
import wave
import os

def wav_recorder(frames, count, audio_q):
    # save the audio frames as .wav file
    fname = str(count)+".wav"
    p_fname = os.path.join('output','raw_audio',fname)
    
    wavefile = wave.open(p_fname,'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(2)
    wavefile.setframerate(44100)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    audio_q.put(count)
    
    
def print_available_mics():
    audio = pyaudio.PyAudio()
    #Print out available mics
    for ii in range(audio.get_device_count()):
        print(audio.get_device_info_by_index(ii).get('name'))


def record_process(audio_q):

    frames_1 = []
    frames_2 = []
    frames = []


    #initialize microphone
    audio = pyaudio.PyAudio()
   
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 5 # seconds to record
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                          input_device_index = dev_index,input = True, \
                            frames_per_buffer=chunk)

    process_running = False
    frame_switch_flag = False
    count = 0
    
    while (1):
                # loop through stream and append audio chunks to frame array
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = stream.read(chunk)

            if (frame_switch_flag) == False:
                frames_1.append(data)
            else:
                frames_2.append(data)
        #start wave file process
        if (frame_switch_flag) == False:
            frames = frames_1.copy()
            frame_switch_flag = True
            frames_2.clear()
        else:
            frames = frames_2.copy()
            frame_switch_flag = False
            frames_1.clear()

        #init subprcss
        wav_prcss = multiprocessing.Process(target=wav_recorder, args=(frames,count,audio_q,))
        wav_prcss.start()
        wav_prcss.join()

        count+=1
        
        





"""
# stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
stream.close()
p.terminate()    
"""
