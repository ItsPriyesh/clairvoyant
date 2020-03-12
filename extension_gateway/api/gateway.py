import multiprocessing
import traceback
import json

from flask_restplus import fields, reqparse
from maxfw.core import MAX_API, CustomMAXAPI
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


input_parser = MAX_API.parser()
input_parser.add_argument('x-packet')

expected_response = MAX_API.model('Response', {
    'status': fields.String(required=True, description='Response status message')
})


gateway = RXTXGateway()

"""
	GatewayAPI is intended to handle any incoming data packets that are to be forwarded through
	the RXTXGateway to some reciving LoRa module.
"""
class GatewayAPI(CustomMAXAPI):

	@MAX_API.expect(input_parser)
	@MAX_API.marshal_with(expected_response)
	def post(self):
		result = {'status': 'error'}

		args = input_parser.parse_args()
		parsed_packet = eval(args['x-packet'])

		# Need to convert the packet back into a packet that can be transmitted through 
		# Clairyoant LoRa Mesh Network

		gateway.get_input_queue().put(parsed_packet)

		result['status'] = 'ok'
		return result





