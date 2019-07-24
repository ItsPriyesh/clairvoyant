import grpc
import clairvoyant
import traceback

from clairvoyant_data import AckPayload
from clairvoyant_data import PacketBuilder
from clairvoyant_data import Packet
from gen import clairvoyant_pb2 as grpc_model
from gen import clairvoyant_pb2_grpc as grpc_service
from time import time

class ClairvoyantRPCService:

	_DEFAULT_NODE_ID = "DEFAULT"
	_DEFAULT_TIMESTAMP = round(1563073962.387557)
	_DEFAULT_ML_CLASSIFICATION = 'DEFAULT_CLASS'
	_DEFAULT_CONFIDENCE = 100.0
	_DEFAULT_RETRY_COUNT = 1000
	_DEFAULT_HOP_COUNT = 1000
	_DEFAULT_BATTERY_LEVEL = 100

	_DEFAULT_PARAMS = {
		"node_id" : _DEFAULT_NODE_ID,
		"timestamp" : _DEFAULT_TIMESTAMP,
		"classification" : _DEFAULT_ML_CLASSIFICATION,
		"confidence" : _DEFAULT_CONFIDENCE,
		"retry_count" : _DEFAULT_RETRY_COUNT,
		"hop_count" : _DEFAULT_HOP_COUNT,
		"battery_level" : _DEFAULT_BATTERY_LEVEL
	}

	"""
	Initialize Clairyoant gprc client stub.
	"""
	def __init__(self):
		self.channel = grpc.insecure_channel(":".join([clairvoyant.RPC_ADDRESS, clairvoyant.RPC_PORT]))
		self.stub = grpc_service.ClairvoyantServiceStub(self.channel)


	"""
	Check if there all expected parameters are present.
	If expected parameters are missing, add default parameters.
	"""
	def _validate_params_and_set_default(self, obj, *args):
		print("validating params {} with {}".format(obj, args))
		missing = list(args[:])
		params = {}
		for arg in args:
			# print("SATHOSHIK {}".format(arg))
			try:
				if not arg in obj:
					# print("CHECKING missing array {}".format(missing))
					params[arg] = ClairvoyantRPCService._DEFAULT_PARAMS[arg]
				else:			
					# print("EXTRACTING PARAM")
					missing.remove(arg)
					params[arg] = obj[arg]
			except Exception as e:
				traceback.print_exc()
				print("ERROR {}".format(e))
				pass

		missing_str = ",".join(missing)
		#TODO(Sathoshi): Add logging library
		if (len(missing) > 0):
			print("Expected params [{}], missing params [{}]".format(",".join(args), missing_str))

		# print("defaults appended {}".format(params))
		return params

	"""
	Note: This function sets default values for any missing arguments.
	Expected arguments:
		DataPoint {
		    string node_id = 1;
		    string message_id = 2;
		    int64 timestamp = 3;
		    string classification = 4;
		    float confidence = 5;
		    int32 retry_count = 6;
		    int32 hop_count = 7;
	    }
	"""
	def create_data_point(self, packet):
		# convert packet into a hashmap?
		#TODO(Sathoshi) 
		print("about to send data point to rpc")
		params = self._validate_params_and_set_default(
			packet.to_dict(), "node_id", 
			"message_id", 
			"timestamp", 
			"classification", 
			"confidence",
			"retry_count",
			"hop_count")
		print("added defaults {}".format(params))
		try:
			datapoint = grpc_model.DataPoint(**params)

			ack = self.stub.CreateDataPoint(datapoint)
			ack_packet = PacketBuilder()
			ack_packet.set_type("ACK")
			ack_packet.set_node_id(ack.node_id)
			ack_packet.set_message_id(ack.message_id)
			ack_packet.set_payload(AckPayload())
			ack_packet.set_ttl()
			ack_packet.set_retry_count(0)
			ack_packet.set_hop_count(0)

			return ack_packet.build()
		except Exception as e:
			traceback.print_exc()
			raise(e)

	"""
	Note: This function sets default values for any missing arguments.
	Expected arguments:
		HeartBeat {
	    string node_id = 1;
		    string message_id = 2;
		    int64 timestamp = 3;
		    float battery_level = 4;
		    int32 retry_count = 5;
		    int32 hop_count = 6;
	    }
	"""
	def heart_beat(self, packet):

		print("about to send heart beat to rpc")
		params = self._validate_params_and_set_default(
			packet.to_dict(), 
			"node_id", 
			"message_id", 
			"timestamp", 
			"battery_level", 
			"retry_count",
			"hop_count")
		print("added defaults {}".format(params))
		try:
			heart_beat = grpc_model.Heartbeat(**params)

			ack = self.stub.Ping(heart_beat)
			ack_packet = PacketBuilder()
			ack_packet.set_type("ACK")
			ack_packet.set_node_id(ack.node_id)
			ack_packet.set_message_id(ack.message_id)
			ack_packet.set_payload(AckPayload())
			ack_packet.set_ttl()
			ack_packet.set_retry_count(0)
			ack_packet.set_hop_count(0)
			
			return ack_packet.build()
		except Exception as e:
			traceback.print_exc()
			raise(e)


