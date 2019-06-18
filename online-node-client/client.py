import grpc
from gen import clairvoyant_pb2 as grpc_model
from gen import clairvoyant_pb2_grpc as grpc_service
from time import time

channel = grpc.insecure_channel("localhost:8080")
stub = grpc_service.ClairvoyantServiceStub(channel)

datapoint = grpc_model.DataPoint(id=1, timestamp=round(time()))
ack = stub.CreateDataPoint(datapoint)
print(ack)


