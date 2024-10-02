"""Web backend for the bench"""

import os
import threading
from typing import List, Union

import adi
import numpy as np
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import supported_devices from the data_capture module
from bench.keysight.dwta.data_capture import supported_devices


class SharedState:
    def __init__(self):
        self.buffer = None
        self.device = None


state = SharedState()


def read_state(prop):
    global state
    return getattr(state, prop)


def write_state(prop, value):
    global state
    setattr(state, prop, value)


class BufferWrite(BaseModel):
    uri: str
    device: str
    channel: int
    data_filename: str
    do_scaling: bool
    cycle: bool
    data_complex: bool
    properties: List[str]


app = FastAPI()

file_location = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(file_location, "templates"))


@app.post("/clearbuffer")
async def clearbuffer():
    write_state("buffer", None)
    write_state("device", None)
    return {"status": "ok"}


@app.post("/writebuffer")
async def writebuffer(bufferwrite: BufferWrite):
    # print(bufferwrite)
    # print(bufferwrite.channels)

    # Checks
    if bufferwrite.device not in supported_devices:
        return {
            "status": f"Device not supported: {bufferwrite.device}. Supported devices: {supported_devices}"
        }

    # Create device
    device = getattr(adi, bufferwrite.device)(bufferwrite.uri)
    device.tx_enabled_channels = [bufferwrite.channel]
    for prop in bufferwrite.properties:
        key, value = prop.split("=")
        if not hasattr(device, key):
            return {"status": f"Device does not have attribute: {key}"}
        if value.isdigit():
            value = int(value)
        setattr(device, key, value)

    # Read data from file
    # CSV file where first two rows are sample rate and center frequency
    # Rest of the rows are IQ data in format: I, Q
    with open(bufferwrite.data_filename, "r") as f:
        sample_rate = int(f.readline().split("=")[1].replace("\n", ""))
        center_frequency = int(float(f.readline().split("=")[1].replace("\n", "")))
        i_list = []
        q_list = []
        for line in f:
            i, q = line.split(",")
            i = float(i)
            q = float(q)
            i_list.append(int(i))
            q_list.append(int(q))
        complex_data = np.array(i_list) + 1j * np.array(q_list)

    if type(device) in [adi.Pluto]:
        device.sample_rate = sample_rate
        device.tx_lo = center_frequency
    elif type(device) in [adi.ad9081, adi.ad9084]:
        assert device.tx_sample_rate == sample_rate, "Sample rate mismatch"

    # Write data to buffer
    device.tx_cyclic_buffer = bufferwrite.cycle
    device.tx(complex_data)

    # Save device state
    write_state("device", device)

    return {"status": "ok"}


@app.get("/help/{id}", response_class=HTMLResponse)
async def help(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="help.html", context={"id": id}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
