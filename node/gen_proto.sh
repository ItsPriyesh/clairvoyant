rm -rf gen
mkdir gen
python3 -m grpc_tools.protoc -I../backend/src/main/proto --python_out=./gen --grpc_python_out=./gen ../backend/src/main/proto/clairvoyant.proto
sed -i '' -e 's/^\(import.*_pb2\)/from . \1/' gen/*grpc.py

