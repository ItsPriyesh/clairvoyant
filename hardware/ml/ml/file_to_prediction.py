from sklearn.preprocessing import LabelEncoder
import pickle
from keras.utils import to_categorical
import pandas as pd 
import os
import numpy as np
import librosa
from keras.models import load_model
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")
AUDIO_TESTING_PATH = '/Users/justin/desktop/school/4th_year/fydp/audio_samples/noise/'
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
	global le
	global model
	prediction_feature = extract_features(file_path)
	prediction_feature = prediction_feature.reshape(1, NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS)
	predicted_vector = model.predict_classes(prediction_feature)
	predicted_class = le.inverse_transform(predicted_vector)
	keys = le.classes_
	values = le.transform(le.classes_)
	classes_dict = dict(zip(keys, values))
	predicted_proba_vector = model.predict_proba(prediction_feature)
	listed = predicted_proba_vector[0]
	count = 0
	for key, value in classes_dict.items():
		classes_dict[key] = listed[count]
		count+=1

	return classes_dict

def extract_features(file_name):
	max_pad_len = 174

	try:
		audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast', duration=4.0) 
		if (max(audio) != 0.0):
			trimmed_audio, index = librosa.effects.trim(audio, top_db = 20)

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
	os.chdir(AUDIO_TESTING_PATH)
	for filename in os.listdir(AUDIO_TESTING_PATH):
		print(filename)
		prediction = predict_file(filename)
		print("The predicted labels for {0} are: ".format(filename), prediction)

