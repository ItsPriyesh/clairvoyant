#
# Download model:
# wget -nv --show-progress --progress=bar:force:noscroll https://max-assets-prod.s3.us-south.cloud-object-storage.appdomain.cloud/max-audio-classifier/1.0.0/assets.tar.gz --output-document=assets/assets.tar.gz
# Extract the model tar and put the files in a folder called 'assets' in the same directory as this file.
#

import clairvoyant_data
import clairvoyant
import os
import multiprocessing
import time
import warnings
import tensorflow as tf
import time
import pandas as pd
import numpy as np
import librosa
import traceback

from ml.core.model import ModelWrapper
# from sklearn.preprocessing import LabelEncoder
# from keras.utils import to_categorical
# from keras.models import load_model
from clairvoyant_data import PacketBuilder
from clairvoyant_data import PacketBuilder

MODEL_PATH = os.path.join('ml','assets','weights.best.resampled_cnn6.hdf5')
CSV_PATH = os.path.join('ml','assets','final_labeled_df.csv')

## fixed params
NUM_ROWS = 40
NUM_COLUMNS = 174
NUM_CHANNELS = 1
# CONFIDENCE_LEVEL = 0.5

def init(ml_q,ml_init_q):

    print("Initializing Machine Learning Process...")
    
    files = []
    warnings.filterwarnings("ignore")
    tf.logging.set_verbosity(tf.logging.ERROR)

    model_wrapper = ModelWrapper()

    while (1):
        
        #check for new files
        if (ml_q.empty() == False):
            files.append(str(ml_q.get()) + ".wav")
            
        if (len(files) > 0):
            print("file " + str(files[0]))
            file_path = os.path.join('output','processed_audio',files[0])

            ## IBM MODEL
            ibm_packet = ibm_model(file_path, model_wrapper)
            if ibm_packet != "NOISE":
                ml_init_q.put(ibm_packet)

            del files[0]

def ibm_model(file_path, model_wrapper):
    # model_wrapper = ModelWrapper()
    IBM_DF = model_wrapper.indices
    LABEL_MAPPING = IBM_DF[['display_name', 'class']].set_index('display_name').T.to_dict('dict')
    ibm_predictions = model_wrapper._predict(file_path, 0)
    glob_df = pd.DataFrame(columns=['sub_label', 'confidence', 'label'])

    for el in ibm_predictions:
        sub_label = el[1]
        num = el[2]
        new_label = LABEL_MAPPING.get(sub_label)['class']
        temp_df = pd.DataFrame([[sub_label, num, new_label]], columns=['sub_label', 'confidence', 'label'])
        glob_df = glob_df.append(temp_df)

    total_confidence = glob_df['confidence'].sum()
    sub_label = ibm_predictions[0][1]
    prediction = LABEL_MAPPING.get(sub_label)['class']

    pred_df = glob_df.loc[glob_df['label'] == str(prediction)]
    prediction_sum = pred_df['confidence'].sum()
    normalized_ratio = prediction_sum / total_confidence

    # print('pred confidence: ', prediction_sum)
    # print("total confidence: ", total_confidence)
    # print("ratio: ", ratio)
    # confidence = ibm_predictions[0][2]

    print("\r\nIBM prediction: {}, IBM confidence: {}\r\n".format(prediction, normalized_ratio))

    built_packet = ''
        
    if str(prediction) == 'noise':
        built_packet = "NOISE"

    else:
        ans = "i_" + prediction 
        timestamp = round(time.time())
        # ml_payload = clairvoyant_data.MlPayload(_battery_lvl = 100.0, _timestamp = timestamp, _classification = prediction, _confidence = confidence)
        ml_payload = clairvoyant_data.MlPayload()
        ml_payload._battery_lvl = 100.0
        ml_payload._timestamp = timestamp
        ml_payload._classification = ans
        ml_payload._confidence = normalized_ratio
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