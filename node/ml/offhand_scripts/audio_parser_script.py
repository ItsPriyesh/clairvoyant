import os

dir_ = '/Users/justin/desktop/school/4th_year/FYDP/audio'


def delete_bad_audio():
	not_wanted = ['0', '2', '3', '4', '7', '9']
	
	for subdir, dirs, files in os.walk(dir_):
	    for file in files:
	    	print("subdir: ", subdir)
	    	print("dirs: ", dirs)
	    	print("file: ", file)
	    	split_str = file.split("-", 2)
	    	count = 0
	    	for el in split_str:
	    		count+=1

	    		if count == 2 and str(el) in not_wanted:
	    			print(split_str)
	    			print(file)
	    			print("going to remove {0} file".format(file))
	    			cur_path = subdir + '/' + file
	    			print("path: ", cur_path)
	    			os.remove(cur_path)
	    			break

def move_audio():
	for subdir, dirs, files in os.walk(dir_):
	    for file in files:
	    	cur_path = subdir + '/' + file
	    	new_path = dir_ + '/' + file
	    	print("cur_path: ", cur_path)
	    	print("new_path: ", new_path)
	    	os.rename(cur_path, new_path)

if __name__ == "__main__":
	os.chdir(dir_)

	move_audio()


