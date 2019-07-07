
from sklearn.preprocessing import LabelEncoder
import pickle
from keras.utils import to_categorical
import pandas as pd 
import os
import numpy as np
import librosa
from keras.models import load_model
from datetime import datetime
import tensorflow as tf
import warnings
import multiprocessing




def ml_process(ml_q):

        files = []
        warnings.filterwarnings("ignore")
        tf.logging.set_verbosity(tf.logging.ERROR)
        #Initialize ML PROCESS

        MODEL_PATH = os.path.join('ml_model','weights.best.basic_cnn_2.hdf5')
        CSV_PATH = os.path.join('ml_model','testing_noise.csv')

        ## fixed params
        NUM_ROWS = 40
        NUM_COLUMNS = 174
        NUM_CHANNELS = 1

        df = pd.read_csv(CSV_PATH)

        y = np.array(df.class_label.tolist())
        le = LabelEncoder()
        yy = to_categorical(le.fit_transform(y)) 
        model = load_model(MODEL_PATH)
        ml_q.put(1)

        #Actual ML Processing
        while(1):

                

                #check for new files
                if (ml_q.empty() == False):
                    files.append(str(ml_q.get()) + ".wav")

                if (len(files) > 0):
                        print("file " + str(files[0]))
                        file_path = os.path.join('output','processed_audio',files[0])

                
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

                        print (classes_dict)

                        #del from array, (add delete actual file late for garbage)
                        del files[0]

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



