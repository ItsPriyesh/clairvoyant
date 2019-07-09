Online Endpoint Node Client
===========================
This HTTP client runs on the WiFi connected Raspberry Pi node. It sends data collected by other nodes to the server via gRPC with protobuf encoding.

Setup
-----
Python3 and pip required.

Install dependencies via pip:
```
pip install grpcio
pip install grpcio-tools
```

Generate gRPC client code from proto interface:
```
./gen_proto.sh
```

Run client:
```
python3 client.py
```
  
