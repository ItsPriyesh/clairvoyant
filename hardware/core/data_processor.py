import pyaudio
import multiprocessing
import wave
import os
import contextlib

def audio_process(audio_q,ml_q):

    shift = int(176400/2) #2 second
    files = []
    frames_1 = []
    frames_2 = []

    sample_index = 0
    count = 0
    

    while(1):
    
        #check for new files
        if (audio_q.empty() == False):
            files.append(str(audio_q.get()) + ".wav")

        if (len(files) > 0):
            #sample rate is 44100, so 176400 samples in 4 seconds
            
            fname = os.path.join('output','raw_audio',files[0])
            f1 = wave.open(fname,'rb')
            frame_cnt = f1.getnframes()
            #print(frame_cnt)
            
            #Case 1: Current file has 176400 unread samples
            if (sample_index + 176400 <= frame_cnt):
                #read out 176400 frames, put wave file in processed_audio, and
                #call ml and pass file name.  deletes file after
                #processing
                frames_1 = f1.readframes(f1.getsampwidth()*frame_cnt)

                frames_1 = frames_1[sample_index*f1.getsampwidth():f1.getsampwidth()*(sample_index+176400)]


                fname = str(count)+".wav"
                fname = os.path.join('output','processed_audio',fname)
                
                wavefile = wave.open(fname,'w')
                wavefile.setparams(f1.getparams())

                wavefile.writeframes(frames_1)
                wavefile.close()
                f1.close()

                #insert ml func call here..
                ml_q.put(count)
                #print("processed frames count: " +str(len(frames_1)))

                #increment sample index
                sample_index += shift

                if (sample_index >= frame_cnt):
                    #done with fil                    #add delete file here
                    del files[0]
                    sample_index -= frame_cnt
                #print (sample_index)

                    
                count+=1
                

                
            #else, we need to look at next file for part of the 176400 unread samples
            elif (len(files)>1): #make sure there is a 2nd file, else wait

                #read out size - frames from the first file
                frames_1 = f1.readframes(f1.getsampwidth()*frame_cnt)
                frames_1 = frames_1[f1.getsampwidth()*sample_index:]
                f1.close()

                #print("aa" + str(len(frames_1)/2))
                #look at 2nd file
                fname = os.path.join('output','raw_audio',files[1])
                f1 = wave.open(fname,'rb')
                frame_cnt2 = f1.getnframes()
                
                frames_2 = f1.readframes(f1.getsampwidth()*frame_cnt2)
                frames_2 = frames_2[:f1.getsampwidth()*(176400 - (frame_cnt - sample_index))]
                f1.close()

                #print("bb" + str(len(frames_2)/2))


                frames_1 = frames_1 + frames_2

                fname = str(count)+".wav"
                fname = os.path.join('output','processed_audio',fname)
                
                wavefile = wave.open(fname,'wb')
                wavefile.setparams(f1.getparams())
                wavefile.writeframes(frames_1)
                wavefile.close()

                
                #insert ml func call here..
                ml_q.put(count)

                #increment sample index
                sample_index += shift

                if (sample_index >= frame_cnt):
                    #done with file
                    #add delete file here
                    del files[0]
                    sample_index -= frame_cnt

                count+=1

                #print("processead" + " frames count: " + str(count))

            else:
                #last file
                #read out size - frames from the first file
                #frames_1 = f1.readframes(f1.getsampwidth()*frame_cnt)
                #frames_1 = frames_1[f1.getsampwidth()*sample_index:]
                f1.close()
                #print("aa" + str(len(frames_1)/2))
                """
#testing code 
                fname = str(count)+".wav"
                fname = os.path.join('output','processed_audio',fname)
                
                wavefile = wave.open(fname,'wb')
                wavefile.setparams(f1.getparams())
                wavefile.writeframes(frames_1)
                wavefile.close()

                
                #insert ml func call here..

                #increment sample index
                sample_index += shift

                if (sample_index >= frame_cnt):
                    #done with file
                    del files[0]
                    sample_index -= frame_cnt
                    break

                count+=1
                print(count)

                
                #print("processcead" + " frames count: " + str(count))

            #print(len(files))
        

     



    
def test_audio_processor():
    global audio_file_count
    dir_name = os.path.join('output','raw_audio')

    files_copy = os.listdir(dir_name)
    print(files_copy)
    audio_file_count=len(files_copy)
        #check for new files
    audio_process()


    print("compiled")
    dir_name = os.path.join('output','raw_audio')
    files = os.listdir(dir_name)
    files = sorted(files,key=lambda x: int(os.path.splitext(x)[0]))

    count = 0

    for file in files:
        dir_name = os.path.join('output','raw_audio',file)

        with contextlib.closing(wave.open(dir_name,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            print(str(count) + " " + str(frames))
            count+=1

    count = 0
    print("processed")
    dir_name = os.path.join('output','processed_audio')
    files = os.listdir(dir_name)
    files = sorted(files,key=lambda x: int(os.path.splitext(x)[0]))

    for file in files:
        dir_name = os.path.join('output','processed_audio',file)

        with contextlib.closing(wave.open(dir_name,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            print(str(count) + " " + str(frames))
            count+=1


"""
