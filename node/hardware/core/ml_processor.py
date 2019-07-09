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

def ml_process(ml_q,ml_init_q):

    files = []
    warnings.filterwarnings("ignore")
    tf.logging.set_verbosity(tf.logging.ERROR)

    model_wrapper = ModelWrapper()

    ml_init_q.put(1)

    print("ML: Entering superloop")
    while (1):
        
        #check for new files
        if (ml_q.empty() == False):
            files.append(str(ml_q.get()) + ".wav")
            
        if (len(files) > 0):
                print("file " + str(files[0]))
                file_path = os.path.join('output','processed_audio',files[0])
    
                predictions = model_wrapper._predict(file_path, 0)
                print(predictions)
                del files[0]
