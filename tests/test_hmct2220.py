import pytest
import bench
import os

PORT = os.environ.get("PORT", 54321)
DEVICE_IP = os.environ.get("DEVICE_IP", "192.168.1.198")
VISA_ADDR = f"TCPIP::{DEVICE_IP}::{PORT}::SOCKET"


def test_connect():
    
    # Test the connection to the device
    sg = bench.hittite.HMCT2220(visa_address=VISA_ADDR)
    assert sg is not None