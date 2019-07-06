#
# Download model:
# wget -nv --show-progress --progress=bar:force:noscroll https://max-assets-prod.s3.us-south.cloud-object-storage.appdomain.cloud/max-audio-classifier/1.0.0/assets.tar.gz --output-document=assets/assets.tar.gz
# Extract the model tar and put the files in a folder called 'assets' in the same directory as this file.
#
from core.model import ModelWrapper

input = "/Users/priyesh/Desktop/test/3.wav"
model_wrapper = ModelWrapper()
predictions = model_wrapper._predict(input, 0)
print(predictions)
