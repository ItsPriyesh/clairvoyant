import uuid
"""
Expected Packet structure
{
    type: [HEART_BEAT, ML_CLASS, ACK],
    node_id: ,
    message_id: 1,
    payload: { /* follow rpc standard */},
    ttl: 10000
}
"""
class Packet:

	VALID_EVENT_TYPES = ["HEART_BEAT", "ML_CLASS"]
	VALID_ACK_TYPES = ["ACK"]
	VALID_TYPES = VALID_ACK_TYPES + VALID_EVENT_TYPES

	_DEFAULT_TTL = 10000 #ms

	def __init__(self, type = None, node_id = None, message_id = None, payload = None, ttl = None):
		self._strict_arg_validate(type, node_id, message_id, payload, ttl)

		self._type = type
		self._node_id = node_id
		self._message_id = message_id
		self._payload = payload
		self._ttl = ttl

	def __str__(self):
		return 'Packet [type:{}, node_id:{}, message_id:{}, payload:{}, ttl:{}]'.format(self._type, self._node_id, self._message_id, self._payload, self._ttl)

	def get_type(self):
		return self._type

	def get_message_id(self):
		return self._message_id

	def get_node_id(self):
		return self._node_id

	def type_arg_validate(t):
		if t is None:
			raise ValueError("Packet Type not specified")
		elif not isinstance(t, str):
			raise ValueError("Packet is of invalid type")
		elif len([t for tt in Packet.VALID_TYPES if(tt in t)]) == 0:
			raise ValueError("Packet Type not recognized. Type must be one of {}".format(', '.join(Packet.VALID_TYPES)))

	def payload_arg_validate(payload):
		#TODO(Sathoshi): Strict typed handling		
		if (payload is None) or (isinstance(payload, dict) and payload == {}):
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

	def _strict_arg_validate(self, t, node_id, message_id, payload, ttl):
		# check if arguments have a type and data dictionary.
		Packet.type_arg_validate(t)
		Packet.payload_arg_validate(payload)
		Packet.node_id_arg_validate(node_id)
		Packet.message_id_arg_validate(message_id)
		Packet.ttl_arg_validate(ttl)

class PacketBuilder:

	def __init__(self):
		self._type = None
		self._node_id = None
		self._message_id = None
		self._payload = None
		self._ttl = None

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

	def build(self):
		return Packet(type = self._type, node_id = self._node_id, message_id = self._message_id, payload = self._payload, ttl = self._ttl)

	def parseFromSerial(self):
		#TODO(Akaash): Parse the data that is recieved from LoRa side into a Packet before adding into comm_processor input q.
		pass

