import clairvoyant
import clairvoyant_data
import os
import multiprocessing
import warnings
import tensorflow as tf
import time
import pandas as pd
import numpy as np
import librosa
import traceback

from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import load_model
from clairvoyant_data import PacketBuilder
from clairvoyant_data import PacketBuilder

MODEL_PATH = os.path.join('ml','assets','weights.best.resampled_cnn6.hdf5')
CSV_PATH = os.path.join('ml','assets','final_labeled_df.csv')

## fixed params
NUM_ROWS = 40
NUM_COLUMNS = 174
NUM_CHANNELS = 1
# CONFIDENCE_LEVEL = 0.5

JUSTIN_DF = pd.read_csv(CSV_PATH)
y = np.array(JUSTIN_DF.class_label.tolist())
le = LabelEncoder()
yy = to_categorical(le.fit_transform(y)) 
# JUSTIN_MODEL = load_model(MODEL_PATH)

def justin_model(file_path):
    prediction_feature = extract_features(file_path)

    prediction_feature = prediction_feature.reshape(1, NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS)
    JUSTIN_MODEL = load_model(MODEL_PATH)
    predicted_vector = JUSTIN_MODEL.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    keys = le.classes_
    values = le.transform(le.classes_)
    classes_dict = dict(zip(keys, values))
    predicted_proba_vector = JUSTIN_MODEL.predict_proba(prediction_feature)
    listed = predicted_proba_vector[0]
    count = 0
    
    for key, value in classes_dict.items():
        classes_dict[key] = listed[count]
        count+=1

    predictions = sorted(classes_dict.items(), key=lambda x: x[1], reverse=True)
    ans = predictions[0][0]
    confidence = predictions[0][1]
    built_packet = ''

    print("\r\nJustin prediction: {}, Justin confidence: {}\r\n".format(ans, confidence))
    
    if str(ans) == 'noise': 
        built_packet = "NOISE"
    
    else:
        timestamp = round(time.time())
        prediction = "j_" + ans
        # ml_payload = clairvoyant_data.MlPayload(_battery_lvl = 100.0, _timestamp = timestamp, _classification = prediction, _confidence = confidence)
        ml_payload = clairvoyant_data.MlPayload()
        ml_payload._battery_lvl = 100.0
        ml_payload._timestamp = timestamp
        ml_payload._classification = prediction
        ml_payload._confidence = confidence
        ml_packet = PacketBuilder().set_type("ML_CLASS").set_node_id(clairvoyant.CURRENT_NODE).set_message_id().set_payload(ml_payload).set_ttl().set_retry_count().set_hop_count()
        built_packet = ml_packet.build()
    
    return built_packet

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
        traceback.print_exc()
        print("ERROR: Cannot parse the following file: ", file_name)
        return None

    return mfccs

if __name__ == '__main__':

    print("Initializing Machine Learning Process...")

    # Load a new file, and try to classify it using the IBM model. 

    warnings.filterwarnings("ignore")
    tf.logging.set_verbosity(tf.logging.ERROR)

    prefix = 0;

    while (1):
        
        processed_audio_file = str(prefix) + ".wav"

        print("Loading audio from {}..".format(processed_audio_file))

        file_path = os.path.join('output','processed_audio', processed_audio_file)

        justin_packet = justin_model(file_path)

        print(justin_packet)

        prefix+=1



