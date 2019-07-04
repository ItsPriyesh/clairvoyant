import model
import processing
import os
import pandas as pd 
from keras.utils.vis_utils import plot_model
from keras.models import Sequential
import numpy as np
import re
import pickle
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

if __name__ == "__main__":
	df = pd.read_csv("feature_df.csv")

	with open ('MFCC_Feature_Array', 'rb') as fp:
		mfcc_features = pickle.load(fp)
	
	df['feature'] = mfcc_features

	feature_col = df.feature.tolist()
	# feature_col = np.array(df.feature,dtype=np.float32)
	X = np.array(feature_col)
	y = np.array(df.class_label.tolist())

	le = LabelEncoder()
	yy = to_categorical(le.fit_transform(y)) 
	x_train, x_test, y_train, y_test, yy = model.create_train_test_splits(X, yy)

	"""
	## For Debugging ##
	print("x train shape: ", x_train.shape)
	print("x test shape: ", x_test.shape)
	print("y train shape: ", y_train.shape)
	print("y test shape: ", y_test.shape)
	"""

	"""
	## For Opening Pre-Trained Model History ## 
	f = open('history.pckl', 'rb')
	history = pickle.load(f)
	f.close()
	"""

	"""
	## For Running Pre-Trained Model and Running Inferences ##
	cnn_model = model.load_pretrained_model()
	cnn_model.fit(x_train, y_train, batch_size=245, epochs=1)
	model.print_prediction(cnn_model, le)
	"""

	"""
	## For Running Model From Scratch (Training and Evaluating) ##
	cnn_model = model.build_model(yy)
	compiled_model = model.compile_model(cnn_model)
	summarized_model = model.summarize_model(cnn_model)
	model.evaluate_model(cnn_model, x_train, y_train)
	trained_model = model.train_model(cnn_model, x_train, x_test, y_train, y_test)
	#model.evaluate_model(trained_model, x_train, y_train, 'training')
	#model.evaluate_model(trained_model, x_test, y_test, 'testing')
	model.plot_model_stats(trained_model)
	"""

	# plot_model(model, to_file='model.png')


