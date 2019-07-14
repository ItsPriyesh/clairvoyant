import grpc
from gen import clairvoyant_pb2 as grpc_model
from gen import clairvoyant_pb2_grpc as grpc_service
from time import time

class ClairvoyantRPCService:

	_RPC_PORT = '8081'
	_RPC_ADDRESS = 'localhost'

	_DEFAULT_ID = 1
	_DEFAULT_NODE_ID = 1
	_DEFAULT_TIMESTAMP = round(1563073962.387557)
	_DEFAULT_EVENT_TYPE = 'default'
	_DEFAULT_CONFIDENCE = 100.0
	_DEFAULT_BATTERY_LEVEL = 100

	_DEFAULT_PARAMS = {
		"id" : _DEFAULT_ID,
		"node_id" : _DEFAULT_NODE_ID,
		"timestamp" : _DEFAULT_TIMESTAMP,
		"event_type" : _DEFAULT_EVENT_TYPE,
		"confidence" : _DEFAULT_CONFIDENCE,
		"battery_level" : _DEFAULT_BATTERY_LEVEL
	}

	"""
	Initialize Clairyoant gprc client stub.
	"""
	def __init__(self):
		self.channel = grpc.insecure_channel(":".join([ClairvoyantRPCService._RPC_ADDRESS, ClairvoyantRPCService._RPC_PORT]))
		self.stub = grpc_service.ClairvoyantServiceStub(self.channel)

	"""
	Check if there all expected parameters are present.
	If expected parameters are missing, add default parameters.
	"""
	def _validate_params_and_set_default(self, obj, *args):
		missing = args[:];
		params = {}
		for arg in args:
			try:
				if arg not in obj:
					missing.remove(arg)
				else:
					params[args] = obj[args]
					continue
			except:
				pass
			params[arg] = ClairvoyantRPCService._DEFAULT_PARAMS[arg]

		missing_str = ",".join(missing)
		#TODO(Sathoshi): Add logging library
		if (len(missing) > 0):
			print("Expected params [{}], missing params [{}]".format(",".join(args), missing_str))

		return params

	"""
	Note: This function sets default values for any missing arguments.
	Expected arguments:
		DataPoint {
		    int32 id = 1;
		    int32 node_id = 2;
		    int64 timestamp = 3;
		    string event_type = 4;
		    float confidence = 5;
	    }
	"""
	def create_data_point(self, obj):
		params = self._validate_params_and_set_default(obj, "id", "node_id", "timestamp", "event_type", "confidence")
		datapoint = grpc_model.DataPoint(**params)
		try:
			return self.stub.CreateDataPoint(datapoint)
		except Exception as e:
			raise(e)

	"""
	Note: This function sets default values for any missing arguments.
	Expected arguments:
		HeartBeat {
		    int32 id = 1;
		    int64 timestamp = 2;
		    float battery_level = 3;
	    }
	"""
	def heart_beat(self, obj):
		params = self._validate_params_and_set_default(obj, "id", "timestamp", "battery_level")
		heart_beat = grpc_model.Heartbeat(**params)
		try:
			return self.stub.Ping(heart_beat)
		except Exception as e:
			raise(e)


