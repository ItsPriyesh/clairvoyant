# Clairvoyant Node

## Setting up an Raspberry Pi
 1. **Download and unzip Raspbian stretch lite** [https://www.raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/)
 2. **Follow instructions to flash SD card and change config.txt file to add uart**  [https://learn.sparkfun.com/tutorials/headless-raspberry-pi-setup/all](https://learn.sparkfun.com/tutorials/headless-raspberry-pi-setup/all)
 3. **Install USB to UART drivers** [https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)
 4. **Set up networking connection via UART** [https://www.instructables.com/id/Connect-the-Raspberry-Pi-to-network-using-UART/](https://www.instructables.com/id/Connect-the-Raspberry-Pi-to-network-using-UART/)
 5. **Set up ssh keys for AWS Server**
 6. **Start ssh tunnel cron job**
 `crontab -e`
 `*/1 * * * * ~/clairvoyant/hardware/ssh_tunnel.sh > ~/tunnel.log 2>&1`


## Online Endpoint Node Client
This HTTP client runs on the WiFi connected Raspberry Pi node. It sends data collected by other nodes to the server via gRPC with protobuf encoding.

## Setup
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
  
