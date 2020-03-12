import uuid
"""
Expected Packet structure
{
    type: [HEART_BEAT, ML_CLASS, MOTION_EVENT, ACK],
    node_id: ,
    message_id: 1,
    payload: { /* follow rpc standard */},
    ttl: 10000
}
"""
class Packet:

	VALID_EVENT_TYPES = {"HEART_BEAT", "ML_CLASS", "MOTION_EVENT"}
	VALID_ACK_TYPES = {"ACK"}
	VALID_TYPES = VALID_ACK_TYPES | VALID_EVENT_TYPES

	_DEFAULT_TTL = 10000 #ms

	def __init__(
		self, 
		type = None, 
		node_id = None, 
		message_id = None, 
		payload = None, 
		ttl = None, 
		hop_count = None, 
		retry_count = None
		):

		self._strict_arg_validate(type, node_id, message_id, payload, ttl, retry_count, hop_count)

		self._type = type
		self._node_id = node_id
		self._message_id = message_id
		self._payload = payload
		self._ttl = ttl
		self._hop_count = hop_count
		self._retry_count = retry_count

	def __str__(self):
		return 'Packet [type:{}, node_id:{}, message_id:{}, payload:{}, ttl:{}, retry_count:{}, hop_count:{}]'.format(self._type, self._node_id, self._message_id, self._payload, self._ttl, self._retry_count, self._hop_count)

	def get_type(self):
		return self._type

	def get_message_id(self):
		return self._message_id

	def get_node_id(self):
		return self._node_id

	def get_hop_count(self):
		return self._hop_count

	def to_dict(self):
		first_class_params = {"type": self._type, "node_id": self._node_id, "message_id": self._message_id, "ttl": self._ttl, "hop_count": self._hop_count, "retry_count": self._retry_count}
		first_class_params.update(self._payload.to_dict())
		return first_class_params

	def increment_retry_count(self):
		self._retry_count = self._retry_count + 1

	def increment_hop_count(self):
		self._hop_count = self._hop_count + 1

	def type_arg_validate(t):
		if t is None:
			raise ValueError("Packet Type not specified")
		elif not isinstance(t, str):
			raise ValueError("Packet is of invalid type")
		elif not {t}.issubset(Packet.VALID_TYPES):
			raise ValueError("Packet Type not recognized. Type must be one of {}".format(', '.join(Packet.VALID_TYPES)))

	def payload_arg_validate(payload):
		#TODO(Sathoshi): Strict typed handling		
		if payload is None:
			raise ValueError("Payload is empty")

	def node_id_arg_validate(node_id):
		#TODO(Sathoshi): Strict typed handling
		if node_id is None:
			raise ValueError("Node id not specified")	

	def message_id_arg_validate(message_id):
		#TODO(Sathoshi): Strict typed handling		
		if message_id is None:
			raise ValueError("Message identifier not specified")

	def ttl_arg_validate(ttl):
		#TODO(Sathoshi): Strict typed handling		
		if ttl is None:
			raise ValueError("TTL not specified")

	def hop_count_arg_validate(hop_count):
		#TODO(Sathoshi): Strict typed handling		
		pass

	def retry_count_arg_validate(retry_count):
		#TODO(Sathoshi): Strict typed handling		
		pass


	def _strict_arg_validate(self, t, node_id, message_id, payload, ttl, retry_count, hop_count):
		# check if arguments have a type and data dictionary.
		Packet.type_arg_validate(t)
		Packet.payload_arg_validate(payload)
		Packet.node_id_arg_validate(node_id)
		Packet.message_id_arg_validate(message_id)
		Packet.ttl_arg_validate(ttl)
		Packet.retry_count_arg_validate(retry_count)
		Packet.hop_count_arg_validate(hop_count)

class PacketBuilder:

	def __init__(self):
		self._type = None
		self._node_id = None
		self._message_id = None
		self._payload = None
		self._ttl = None
		self._retry_count = None
		self._hop_count = None

	## Valid packet types are {"HEART_BEAT", "ML_CLASS", "MOTION_EVENT", "ACK"}
	def set_type(self, t):
		Packet.type_arg_validate(t)
		self._type = t
		return self

	def set_node_id(self, node_id):
		Packet.node_id_arg_validate(node_id)
		self._node_id = node_id
		return self

	def set_message_id(self, message_id = None):
		if message_id is None:
			self._message_id = uuid.uuid4().hex
			return self

		Packet.message_id_arg_validate(message_id)
		self._message_id = message_id
		return self

	def set_payload(self, payload):
		Packet.payload_arg_validate(payload)
		self._payload = payload
		return self

	def set_ttl(self, ttl = None):
		if ttl is None:
			self._ttl = Packet._DEFAULT_TTL
			return self

		Packet.ttl_arg_validate(ttl)
		self._ttl = ttl
		return self

	def set_hop_count(self, hop_count = None):
		if hop_count is None:
			self._hop_count = 0
			return self

		Packet.hop_count_arg_validate(hop_count)
		self._hop_count = hop_count
		return self

	def set_retry_count(self, retry_count = None):
		if retry_count is None:
			self._retry_count = 0
			return self

		Packet.retry_count_arg_validate(retry_count)
		self._retry_count = retry_count
		return self

	def build(self):
		return Packet(
			type = self._type,
		 	node_id = self._node_id, 
		 	message_id = self._message_id, 
		 	payload = self._payload, 
		 	ttl = self._ttl, 
		 	hop_count = self._hop_count, 
		 	retry_count = self._retry_count)

	
##message DataPoint {
##    string node_id = 1;
##    string message_id = 2;
##    int64 timestamp = 3;
##    string classification = 4;
##    float confidence = 5;
##    int32 retry_count = 6;
##    int32 hop_count = 7;
##}
class MlPayload:
        
	def __init__(self):
		self._battery_lvl = None
		self._timestamp = None
		self._classification = None
		self._confidence = None

	def __str__(self):
		return '[battery_level:{}, timestamp:{}, classification:{}, confidence:{}]'.format(self._battery_lvl, self._timestamp, self._classification, self._confidence)
		    
	def to_array(self):
		if ((self._battery_lvl == None) or (self._timestamp == None) or (self._classification == None) or (self._confidence == None)):
			raise ValueError("Fields are missing")

		payload = [self._battery_lvl, self._timestamp, self._classification, self._confidence]
		return payload

	def to_dict(self):
		if ((self._battery_lvl == None) or (self._timestamp == None) or (self._classification == None) or (self._confidence == None)):
			raise ValueError("Fields are missing")

		data = {"battery_level": self._battery_lvl, "timestamp": self._timestamp, "classification": self._classification, "confidence": self._confidence}
		return data


	def from_dict(self):
		pass
            
	def from_array(self,array):
		if (len(array) != 4):
			raise ValueError("Incorrect Array length")

		self._battery_lvl = array[0]
		self._timestamp = array[1]
		self._classification = array[2]
		self._confidence = array[3]

		return self

##message DataPoint {
##    string node_id = 1;
##    string message_id = 2;
##    int64 timestamp = 3;
##    string motion_type = 4;
##    string orientation = 5;
##    int32 roll = 6;
##    int32 pitch = 7;
##    int32 yaw = 8;
##    int32 retry_count = 9;
##    int32 hop_count = 10;
##}
class MotionPayload:
        
	def __init__(self):
		self._battery_lvl = None
		self._timestamp = None
		self._motion_type = None
		self._orientation = None
		self._roll = None
		self._pitch = None
		self._yaw = None

	def __str__(self):
		return '[battery_level:{}, timestamp:{}, motion_type:{}, orientation:{}, roll:{}, pitch:{}, yaw:{}]'.format(self._battery_lvl, self._timestamp, self._motion_type, self._orientation , self._roll, self._pitch, self._yaw)
		    
	def to_array(self):
		if ((self._battery_lvl == None) or (self._timestamp == None) or (self._motion_type == None) or (self._orientation == None) or (self._roll == None) or (self._pitch == None) or (self._yaw == None)):
			raise ValueError("Required fields are missing")

		payload = [self._battery_lvl, self._timestamp, self._motion_type, self._orientation , self._roll, self._pitch, self._yaw]
		return payload

	def to_dict(self):
		if ((self._battery_lvl == None) or (self._timestamp == None) or (self._motion_type == None) or (self._orientation == None) or (self._roll == None) or (self._pitch == None) or (self._yaw == None)):
			raise ValueError("Fields are missing")

		data = {"battery_level": self._battery_lvl, "timestamp": self._timestamp, "motion_type": self._motion_type, "orientation": self._orientation, "roll": self._roll, "pitch": self._pitch, "yaw": self._yaw}
		return data


	def from_dict(self):
		pass
            
	def from_array(self,array):
		if (len(array) != 7):
			raise ValueError("Incorrect Array length.. Expected fields are missing")

		self._battery_lvl = array[0]
		self._timestamp = array[1]
		self._motion_type = array[2]
		self._orientation = array[3]
		self._roll = array[4]
		self._pitch = array[5]
		self._yaw = array[6]

		return self
                
                    
##message Heartbeat {
##    string node_id = 1;
##    string message_id = 2;
##    int64 timestamp = 3;
##    float battery_level = 4;
##    int32 retry_count = 5;
##    int32 hop_count = 6;
##}          
class HeartbeatPayload:

	def __init__(self):
		self._battery_lvl = None
		self._timestamp = None

	def __str__(self):
		return '[battery_level:{}, timestamp:{}]'.format(self._battery_lvl, self._timestamp)

	def to_array(self):   
		if ((self._battery_lvl == None) or (self._timestamp == None)):
			raise ValueError("Fields are missing")
		payload = [self._battery_lvl, self._timestamp]
		return payload

	def to_dict(self):
		if ((self._battery_lvl == None) or (self._timestamp == None)):
			raise ValueError("Fields are missing")

		return {"battery_level": self._battery_lvl, "timestamp": self._timestamp}

	def from_dict(self):
		pass

	def from_array(self, array):
		if (len(array)) != 2:
			raise ValueError("Incorrect Array length")

		self._battery_lvl = array[0]
		self._timestamp = array[1]

		return self

class AckPayload:
	pass
##message Ack {
##    string node_id = 1;
##    string message_id = 2; stuff is empty
##
##}
