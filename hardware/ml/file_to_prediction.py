from sklearn.preprocessing import LabelEncoder
import pickle
from keras.utils import to_categorical
import pandas as pd 
import os
import numpy as np
import librosa
from keras.models import load_model

AUDIO_TESTING_PATH = '/Users/justin/desktop/school/4th_year/fydp/testy_hw_dev/clairvoyant/hardware/ml/samples/gunshots.wav'
MODEL_PATH = '/Users/justin/desktop/school/4th_year/FYDP/clairvoyant/online-node-client/ml/src/saved_models/weights.best.basic_cnn_2.hdf5'

## fixed params
NUM_ROWS = 40
NUM_COLUMNS = 174
NUM_CHANNELS = 1

df = pd.read_csv("testing_noise.csv")
with open ('/Users/justin/desktop/school/4th_year/FYDP/updated_feature_outfile', 'rb') as fp:
		mfcc_features = pickle.load(fp)

df['feature'] = mfcc_features
y = np.array(df.class_label.tolist())
le = LabelEncoder()
yy = to_categorical(le.fit_transform(y)) 
model = load_model(MODEL_PATH)

def predict_file(file_path):
	prediction_feature = extract_features(AUDIO_TESTING_PATH) 
	prediction_feature = prediction_feature.reshape(1, NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS)
	predicted_vector = model.predict_classes(prediction_feature)
	predicted_class = le.inverse_transform(predicted_vector)

	predicted_proba_vector = model.predict_proba(prediction_feature)
	predicted_proba = predicted_proba_vector[0]
	for i in range(len(predicted_proba)):
		category = le.inverse_transform(np.array([i]))
		print("category: ", category)
		print(category[0], "\t\t : ", format(predicted_proba[i], '.32f'))
	

	return predicted_class[0]

def extract_features(file_name):
	max_pad_len = 174

	try:
		audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast', duration=4.0) 
		if (max(audio) != 0.0):
			trimmed_audio, index = librosa.effects.trim(audio, top_db = 20)
			print("-----------------------------")
			print("Original audio duration: ", librosa.get_duration(audio))
			print("Trimmed audio duration: ", librosa.get_duration(trimmed_audio))
			print("-----------------------------")
			mfccs = librosa.feature.mfcc(y=trimmed_audio, sr=sample_rate, n_mfcc=40)
			pad_width = max_pad_len - mfccs.shape[1]
			mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
		else:
			print("ERROR: Please input a non-empty audio file")
			return None

	except Exception as e:
		print("ERROR: Cannot parse the following file: ", file_name)
		return None

	return mfccs

if __name__ == "__main__":
	prediction = predict_file(AUDIO_TESTING_PATH)
	print("The predicted label is: ", prediction)

