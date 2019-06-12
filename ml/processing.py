import pandas as pd
import os
import librosa
from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

audio_dir = '/Users/justin/desktop/school/4th_year/FYDP/clairvoyant/ml/audio_samples/gun'

"""
def process_audio(sample):
	## sample rate conversion
	librosa_audio, librosa_sample_rate = librosa.load(sample) 
	scipy_sample_rate, scipy_audio = wav.read(sample) 

	print('Original sample rate:', scipy_sample_rate) 
	print('Librosa sample rate:', librosa_sample_rate)

	## bit depth
	print('Original audio file min~max range:', np.min(scipy_audio), 'to', np.max(scipy_audio))
	print('Librosa audio file min~max range:', np.min(librosa_audio), 'to', np.max(librosa_audio))

	## original audio channel
	plt.figure(figsize=(12, 4))
	plt.plot(scipy_audio)
	plt.show()

	## librosa audio with channels merge
	plt.figure(figsize=(12, 4))
	plt.plot(librosa_audio)
	plt.show()

	## extract MFCC
	mfccs = librosa.feature.mfcc(y=librosa_audio, sr=librosa_sample_rate, n_mfcc=40)
	print(mfccs.shape)
"""

def extract_features(file_name):
    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T,axis=0)
        
    except Exception as e:
        print("Error encountered while parsing file: ", file)
        return None 
     
    return mfccsscaled

if __name__ == "__main__":
	os.chdir(audio_dir)

	for file in os.listdir(audio_dir):
		# process_audio(file)
		extract_features(file)