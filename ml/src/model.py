import processing 
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint 
from sklearn import metrics 
from datetime import datetime 
from sklearn.model_selection import train_test_split 
import matplotlib.pyplot as plt
import pickle
from keras.models import load_model

MODEL_PATH = '/Users/justin/desktop/school/4th_year/FYDP/clairvoyant/ml/src/saved_models/weights.best.basic_cnn_2.hdf5'
AUDIO_TESTING_PATH = '/Users/justin/desktop/school/4th_year/FYDP/extra_audio/gun/gun-trigger-click-01.wav'

## fixed params
NUM_ROWS = 40
NUM_COLUMNS = 174
NUM_CHANNELS = 1

def load_pretrained_model():
	cnn_model = load_model('/Users/justin/desktop/school/4th_year/FYDP/clairvoyant/ml/src/saved_models/weights.best.basic_cnn_2.hdf5')

	return cnn_model

def create_train_test_splits(X, yy):
	x_train, x_test, y_train, y_test = train_test_split(X, yy, test_size=0.2, random_state = 42)

	x_train = x_train.reshape(x_train.shape[0], NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS)
	x_test = x_test.reshape(x_test.shape[0], NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS)

	return x_train, x_test, y_train, y_test, yy

def summarize_model(model):
	model.summary()

def evaluate_model(model, x, y, res_type = "pre-training"):
	score = model.evaluate(x, y, verbose=0)
	accuracy = 100*score[1]

	print("{0} accuracy: %.4f%%".format(res_type) % accuracy)

def build_model(yy):
	# params
	num_labels = yy.shape[1]
	filter_size = 2

	model = Sequential()
	model.add(Conv2D(filters=16, kernel_size=2, input_shape=(NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS), activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))

	model.add(Conv2D(filters=32, kernel_size=2, activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))

	model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))

	model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
	model.add(MaxPooling2D(pool_size=2))
	model.add(Dropout(0.2))
	model.add(GlobalAveragePooling2D())

	model.add(Dense(num_labels, activation='softmax'))

	return model

def compile_model(model):
	return model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

def train_model(model, x_train, x_test, y_train, y_test):
	# history = History()
	num_epochs = 30
	num_batch_size = 256

	checkpointer = ModelCheckpoint(filepath=MODEL_PATH, verbose=1, save_best_only=True)
	start = datetime.now()

	trained_model = model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

	duration = datetime.now() - start
	print("Training completed in time: ", duration)

	print(trained_model.history.keys())

	f = open('history.pckl', 'wb')
	pickle.dump(trained_model.history, f)
	f.close()

	return trained_model

def plot_model_stats(history):
	# summarize history for accuracy
	plt.plot(history.history['acc'])
	plt.plot(history.history['val_acc'])
	plt.title('model accuracy')
	plt.ylabel('accuracy')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper left')
	plt.show()

	# summarize history for loss
	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper left')
	plt.show()

def print_prediction(model, le):
    prediction_feature = processing.extract_features(AUDIO_TESTING_PATH) 
    prediction_feature = prediction_feature.reshape(1, NUM_ROWS, NUM_COLUMNS, NUM_CHANNELS)
    print(prediction_feature)
    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector) 
    print("The predicted class is:", predicted_class[0], '\n') 

    predicted_proba_vector = model.predict_proba(prediction_feature) 
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)): 
    	category = le.inverse_transform(np.array([i]))
    	print(category[0], "\t\t : ", format(predicted_proba[i], '.32f'))
