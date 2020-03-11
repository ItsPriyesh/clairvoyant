import multiprocessing
import traceback

from multiprocessing import Queue
from .comm_processor import init

_INPUT_QUEUE = Queue()
_OUTPUT_QUEUE = Queue()

class RXTXGateway:

	def get_input_queue(self):
		return _INPUT_QUEUE

	def get_output_queue(self):
		return _OUTPUT_QUEUE

	def run(self):
		p = multiprocessing.Process(target=init, args=(self.get_input_queue(), self.get_output_queue()))
		p.start();
