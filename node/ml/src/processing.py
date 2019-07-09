import pandas as pd
import os
import librosa
from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split 

AUDIO_DIR = '/Users/justin/desktop/school/4th_year/FYDP/audio/'

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

def extract_features(file_name):
	max_pad_len = 174

	try:
		audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
		mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
		pad_width = max_pad_len - mfccs.shape[1]
		mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

		print('Librosa sample rate:', sample_rate)
		print('Librosa audio file min~max range:', np.min(audio), 'to', np.max(audio))
		# print(mfccs)
		print(mfccs.shape)
	except Exception as e:
		print("Error encountered while parsing file: ", file_name)
		return None

	return mfccs

def create_df():
	path = os.getcwd() + '/' + "UpdatedUrbanSound.csv"
	df = pd.read_csv(path)

	features = []

	# Iterate through each sound file and extract the features 
	for index, row in df.iterrows():
	    file_name = os.path.join(os.path.abspath(AUDIO_DIR),str(row["slice_file_name"]))
	    class_label = row["class"]
	    data = extract_features(file_name)
	    print(data)
	    features.append([data, class_label])

	features_df = pd.DataFrame(features, columns=['feature','class_label'])
	features_df.to_csv("features_df.csv")
	
	return features_df