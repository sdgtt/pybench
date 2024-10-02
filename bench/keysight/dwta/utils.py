""""Utilities for the Keysight DWTA."""

import os
import subprocess
from typing import List, Union

import adi
import numpy as np


def data_to_iq_datafile(
    device, data: np.ndarray, filename: str, device_check: bool = True
) -> None:
    """Write data to a file in IQ data format.

    Args:
        device: Device object from pyadi-iio library.
        data: The data to write.
        filename: The filename to write to.
        device_check: Check if specific class is supported. Default is True.
    """
    # Checks
    assert data.dtype == np.complex128, "Data must be complex"
    assert device._complex_data, "Device does not support complex data"
    if device_check:
        supported_devices = ["Pluto", "ad9081"]
        assert any(
            dev in device.__class__.__name__ for dev in supported_devices
        ), f"Device not supported. Supported devices: {supported_devices}"

    # Get sample rate and carrier frequencies
    if hasattr(device, "sample_rate"):
        sample_rate = device.sample_rate
    elif hasattr(device, "rx_sample_rate"):
        sample_rate = device.rx_sample_rate
    else:
        raise AttributeError("Device does not have sample rate attribute")

    if type(device) in [adi.Pluto]:
        center_frequency = int(device.rx_lo)  # FIXME
    elif type(device) in [adi.ad9081, adi.ad9084]:
        channel = device.rx_enabled_channels[0]
        f1 = device.rx_channel_nco_frequencies
        f2 = device.rx_main_nco_frequencies
        center_frequency = f1[channel] + f2[channel]
    else:
        raise NotImplementedError("Center frequency not implemented for this device")

    assert device._complex_data, "Device does not support complex data"

    with open(filename, "w") as f:
        f.write(f"SampleRate={sample_rate}\n")
        f.write(f"CenterFrequency={center_frequency}\n")
        for d in data:
            f.write(f"{d.real},{d.imag}\n")

    print(f"Data written to {filename}")
