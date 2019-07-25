import grpc
from gen import clairvoyant_pb2 as grpc_model
from gen import clairvoyant_pb2_grpc as grpc_service
from time import time

channel = grpc.insecure_channel("localhost:8080")
stub = grpc_service.ClairvoyantServiceStub(channel)

datapoint = grpc_model.DataPoint(message_id="fewsssfdsdfsfdsdsdfsdffdfsdsdss", node_id="2", 
	timestamp=round(time()), classification="GUNSHOT", confidence=0.22)
ack = stub.CreateDataPoint(datapoint)
print(ack)

heartbeat = grpc_model.Heartbeat(node_id="1", message_id="nfeihefhefh", timestamp=round(time()),
	battery_level=10.2, retry_count=1, hop_count=1)
ack = stub.Ping(heartbeat)
print(ack)

