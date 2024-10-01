import requests
import os
import numpy as np

# Generate some data
fs = int(1e6)
N = 1024
fc = int(300000 / (fs / N)) * (fs / N)
ts = 1 / float(fs)
t = np.arange(0, N * ts, ts)
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q

# Create CSV file
filename = "iq_data.csv"
with open(filename, "w") as f:
    f.write(f"SampleRate={fs}\n")
    f.write(f"CenterFrequency={fc}\n")
    for i, q in zip(i, q):
        f.write(f"{i},{q}\n")


# Send post request to localhost
url = "http://localhost:8000/writebuffer"
    # uri: str
    # device: str
    # channel: int
    # data_filename: str
    # do_scaling: bool
    # cycle: bool
    # data_complex: bool
    # properties: List[str]

file_location = os.path.dirname(os.path.realpath(__file__))

data = {
    "uri": "ip:pluto.local",
    "device": "Pluto",
    "channel": 0,
    "data_filename": os.path.join(file_location, filename),
    "do_scaling": False,
    "cycle": True,
    "data_complex": True,
    "properties": ["sample_rate=" + str(fs)],
}
r = requests.post(url, json=data)
print(f"Status: {r.status_code}")
print(r.json())

import time
for _ in range(10):
    print(".", end="")
    time.sleep(1)
print()
url = "http://localhost:8000/clearbuffer"
r = requests.post(url)
print(f"Status: {r.status_code}")
