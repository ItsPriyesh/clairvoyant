import multiprocessing

def init(input_q, output_q):

	while(1):
		if(input_q.empty()):
			continue

		print(input_q)
		print(input_q.get())