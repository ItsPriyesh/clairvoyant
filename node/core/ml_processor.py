#
# Download model:
# wget -nv --show-progress --progress=bar:force:noscroll https://max-assets-prod.s3.us-south.cloud-object-storage.appdomain.cloud/max-audio-classifier/1.0.0/assets.tar.gz --output-document=assets/assets.tar.gz
# Extract the model tar and put the files in a folder called 'assets' in the same directory as this file.
#

import clairvoyant_data
import clairvoyant
from ml.core.model import ModelWrapper
import os
import multiprocessing
import time
import warnings
import tensorflow as tf
import datetime

MODEL_PATH = os.path.join('ml','assets','weights.best.resampled_cnn6.hdf5')
CSV_PATH = os.path.join('ml','assets','final_labeled_df.csv')

model_wrapper = ModelWrapper()
IBM_DF = model_wrapper.indices
LABEL_MAPPING = IBM_DF[['display_name', 'class']].set_index('display_name').T.to_dict('dict')

## fixed params
NUM_ROWS = 40
NUM_COLUMNS = 174
NUM_CHANNELS = 1

JUSTIN_DF = pd.read_csv(CSV_PATH)
y = np.array(JUSTIN_DF.class_label.tolist())
le = LabelEncoder()
yy = to_categorical(le.fit_transform(y)) 
JUSTIN_MODEL = load_model(MODEL_PATH)

def init(ml_q,ml_init_q):

    print("Initializing Machine Learning Process...")
    
    files = []
    warnings.filterwarnings("ignore")
    tf.logging.set_verbosity(tf.logging.ERROR)

    print("ML: Entering superloop")
    while (1):
        
        #check for new files
        if (ml_q.empty() == False):
            files.append(str(ml_q.get()) + ".wav")
            
        if (len(files) > 0):
            print("file " + str(files[0]))
            file_path = os.path.join('output','processed_audio',files[0])

            ## JUSTIN MODEL
            justin_packet = justin_model(file_path)
            if justin_packet != "NOISE":
                ml_init_q.put(justin_packet)

            ## IBM MODEL
            ibm_packet = ibm_model(file_path)
            if ibm_packet != "NOISE":
                ml_init_q.put(ibm_packet)

            del files[0]

def justin_model(file_path):
    prediction_feature = extract_features(file_path)
    prediction_feature = prediction_feature.reshape(1, NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS)
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
    prediction = "J " + predictions[0][0]
    confidence = predictions[0][1]
    built_packet = ''

    # print("Justin model prediction: ", prediction)
    # print("Justin model confidence: ", confidence)
    
    if str(prediction) == 'noise':
        built_packet = "NOISE"
    
    else:
        timestamp = datetime.datetime.now().time()
        ml_payload = clairvoyant_data.MlPayload(_battery_lvl = 100, _timestamp = timestamp, _classification = prediction, _confidence = confidence)
        ml_packet = clairvoyant_data.PacketBuilder(_type = "ML_CLASS",_node_id = clairvoyant.CURRENT_NODE, _message_id = None, _payload = ml_payload, _ttl = None)
        built_packet = ml_packet.build()
    
    return built_packet

def ibm_model(file_path):
    ibm_predictions = model_wrapper._predict(file_path, 0)

    # print("IBM model predictions: ", ibm_predictions)

    sub_label = ibm_predictions[0][1]
    prediction = "I " + LABEL_MAPPING.get(sub_label)['class']
    confidence = ibm_predictions[0][2]
    built_packet = ''
        
    if str(prediction) == 'noise':
        built_packet = "NOISE"

    else:
        timestamp = datetime.datetime.now().time()
        ml_payload = clairvoyant_data.MlPayload(_battery_lvl = 100, _timestamp = timestamp, _classification = prediction, _confidence = confidence)
        ml_packet = clairvoyant_data.PacketBuilder(_type = "ML_CLASS",_node_id = clairvoyant.CURRENT_NODE, _message_id = None, _payload = ml_payload, _ttl = None)
        built_packet = ml_packet.build()

    return built_packet