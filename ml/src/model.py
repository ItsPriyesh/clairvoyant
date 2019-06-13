import processing 
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint 
from sklearn import metrics 
from datetime import datetime 

model_path = '/Users/justin/desktop/school/4th_year/FYDP/clairvoyant/ml/saved_models/'

def summarize_model(model, x_test, y_test):
	# Display model architecture summary 
	model.summary()

	# Calculate pre-training accuracy 
	score = model.evaluate(x_test, y_test, verbose=0)
	accuracy = 100*score[1]

	print("Pre-training accuracy: %.4f%%" % accuracy)

def build_model(x_train, x_test):
	# params
	num_rows = 40
	num_columns = 174
	num_channels = 1
	num_labels = processing.yy.shape[1]
	filter_size = 2

	x_train = x_train.reshape(x_train.shape[0], num_rows, num_columns, num_channels)
	x_test = x_test.reshape(x_test.shape[0], num_rows, num_columns, num_channels)

	# Construct model 
	"""
	Architecture:
	4 Conv2D convolution layers
	layer 1 -- input shape of (40, 174, 1), 40 = # MFCC, 174 = #frames with padding, 1 = channel (mono)
	output layer -- dense layer
	"""
	model = Sequential()
	model.add(Conv2D(filters=16, kernel_size=2, input_shape=(num_rows, num_columns, num_channels), activation='relu'))
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

def train_model(model, x_test, y_test):
	num_epochs = 100
	num_batch_size = 32

	checkpointer = ModelCheckpoint(filepath=model_path, verbose=1, save_best_only=True)
	start = datetime.now()

	model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

	duration = datetime.now() - start
	print("Training completed in time: ", duration)

def print_prediction(file_name):
    prediction_feature = processing.extract_feature(file_name) 

    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector) 
    print("The predicted class is:", predicted_class[0], '\n') 

    predicted_proba_vector = model.predict_proba(prediction_feature) 
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)): 
        category = le.inverse_transform(np.array([i]))
        print(category[0], "\t\t : ", format(predicted_proba[i], '.32f'))
