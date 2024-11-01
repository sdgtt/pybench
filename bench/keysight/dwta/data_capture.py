"""Keysight DWTA data capture module."""

import adi

from ..dwta import supported_devices
from .utils import data_to_iq_datafile


def capture_iq_datafile(
    filename: str, device_name: str, channel: int, samples: int, uri: str, **kwargs
) -> None:
    """Capture IQ data to a file.

    Args:
        filename: The filename to write to.
        device_name: The device name.
        channel: The channel to capture data from.
        samples: The number of samples to capture.
        uri: The URI of the device.
        *args: Additional arguments.
        **kwargs: Additional keyword arguments.
    """
    # Checks
    assert (
        device_name in supported_devices
    ), f"Device not supported: {device_name}.\n Supported devices: {supported_devices}"
    assert samples > 0, "Number of samples must be greater than 0"
    if "ip:" not in uri and "usb:" not in uri:
        raise ValueError(f"URI must start with 'ip:' or 'usb:'. Got: {uri}")

    # Create device
    device = getattr(adi, device_name)(uri)

    # Assume kwargs are attributes to set
    for key, value_index in kwargs.items():
        value = value_index["value"]
        index = value_index["index"]
        if not hasattr(device, key):
            raise AttributeError(f"Device does not have attribute: {key}")
        if index == -1:
            print(f"Setting {key} to {value}")
            setattr(device, key, value)
        else:
            prop = getattr(device, key)
            if prop is not list:
                raise ValueError(f"Property {key} is not an array")
            assert index < len(prop), f"Index out of range for {key}"
            prop[index] = value
            print(f"Setting {key}[{index}] to {value}")
            setattr(device, key, prop)


    # Capture data
    device.rx_enabled_channels = [channel]
    device.rx_buffer_size = samples
    data = device.rx()

    # Write data to file
    data_to_iq_datafile(device, data, filename, device_check=False)
