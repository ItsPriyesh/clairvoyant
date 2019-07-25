import grpc
from gen import clairvoyant_pb2 as grpc_model
from gen import clairvoyant_pb2_grpc as grpc_service
from time import time

channel = grpc.insecure_channel("localhost:8080")
stub = grpc_service.ClairvoyantServiceStub(channel)

datapoint = grpc_model.DataPoint(message_id="sss"+str(time()), node_id="2", 
	timestamp=round(time()), classification="VEHICLE", confidence=0.42)
ack = stub.CreateDataPoint(datapoint)
print(ack)


