import bench.hittite as hittite
import argparse

# Get IP address from command line
parser = argparse.ArgumentParser(description='Connect to Hittite HMCT2220')
parser.add_argument('ip', type=str, help='IP address of the device')
# Port with default value 54321
parser.add_argument('--port', type=int, default=54321, help='Port number of the device')
args = parser.parse_args()


# Connect to the device
sg = hittite.HMCT2220(visa_address=f"TCPIP::{args.ip}::{args.port}::SOCKET")

# Print the IDN
print(sg._instr.query("*IDN?"))
