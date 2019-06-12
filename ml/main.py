import model
import processing
import os

if __name__ == "__main__":
	os.chdir(processing.audio_dir)

	for file in os.listdir(processing.audio_dir):
		processing.process_audio(file)
		processing.extract_features(file)
	