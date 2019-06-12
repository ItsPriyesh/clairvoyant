rm clairvoyant_pb2.py clairvoyant_pb2_grpc.py
python3 -m grpc_tools.protoc -I../backend/src/main/proto --python_out=. --grpc_python_out=. ../backend/src/main/proto/clairvoyant.proto

