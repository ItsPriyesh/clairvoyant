import grpc
from gen import clairvoyant_pb2 as grpc_model
from gen import clairvoyant_pb2_grpc as grpc_service
from time import time

channel = grpc.insecure_channel("168.62.177.105:8080")
stub = grpc_service.ClairvoyantServiceStub(channel)

datapoint = grpc_model.DataPoint(message_id="sss"+str(time()), node_id="1", 
	timestamp=round(time()), classification="EXPLOSION", confidence=0.42)
ack = stub.CreateDataPoint(datapoint)
print(ack)

heartbeat = grpc_model.Heartbeat(node_id="1", message_id="nfeihefhefh", timestamp=round(time()),
	battery_level=10.2, retry_count=1, hop_count=1)
ack = stub.Ping(heartbeat)
print(ack)

motionevent = grpc_model.MotionEvent(message_id="eee"+str(time()), node_id="1", 
	timestamp=round(time()), motion_type="EXTERNAL", orientation="UP", roll=120, pitch=40, yaw=90)
ack = stub.CreateMotionEvent(motionevent)
print(ack)

