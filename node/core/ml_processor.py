#
# Download model:
# wget -nv --show-progress --progress=bar:force:noscroll https://max-assets-prod.s3.us-south.cloud-object-storage.appdomain.cloud/max-audio-classifier/1.0.0/assets.tar.gz --output-document=assets/assets.tar.gz
# Extract the model tar and put the files in a folder called 'assets' in the same directory as this file.
#

from ml.core.model import ModelWrapper
import os
import multiprocessing
import time
import warnings
import tensorflow as tf

def init(ml_q,ml_init_q):

    print("Initializing Machine Learning Process...")
    
    files = []
    warnings.filterwarnings("ignore")
    tf.logging.set_verbosity(tf.logging.ERROR)

    MODEL_PATH = os.path.join('ml','assets','weights.best.resampled_cnn6.hdf5')
    CSV_PATH = os.path.join('ml','assets','final_labeled_df.csv')

    model_wrapper = ModelWrapper()

    ## fixed params
    NUM_ROWS = 40
    NUM_COLUMNS = 174
    NUM_CHANNELS = 1

    df = pd.read_csv(CSV_PATH)

    y = np.array(df.class_label.tolist())
    le = LabelEncoder()
    yy = to_categorical(le.fit_transform(y)) 
    model = load_model(MODEL_PATH)

    ml_init_q.put(1)

    print("ML: Entering superloop")
    while (1):
        
        #check for new files
        if (ml_q.empty() == False):
            files.append(str(ml_q.get()) + ".wav")
            
        if (len(files) > 0):
            print("file " + str(files[0]))
            file_path = os.path.join('output','processed_audio',files[0])
            
            # predictions = model_wrapper._predict(file_path, 0)
            # print(predictions)

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

            predictions = sorted(classes_dict.items(), key=lambda x: x[1], reverse=True)
            prediction = predictions[0][0]
            confidence = predictions[0][1]
            print("prediction: ", prediction)
            print("confidence: ", confidence)

            del files[0]
