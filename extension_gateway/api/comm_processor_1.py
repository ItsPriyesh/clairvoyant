import multiprocessing

def init(input_q, output_q):

	while(1):
		if not input_q.empty():
			print(input_q.get())