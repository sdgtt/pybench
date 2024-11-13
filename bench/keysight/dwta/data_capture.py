"""Keysight DWTA data capture module."""

import adi

from ..dwta import supported_devices
from .utils import data_to_iq_datafile


def capture_iq_datafile(
    filename: str, device_name: str, channel: int, side: int, samples: int, plot: bool, uri: str, **kwargs
) -> None:
    """Capture IQ data to a file.

    Args:
        filename: The filename to write to.
        device_name: The device name.
        channel: The channel to capture data from.
        side: The device side to capture data from (AD9084/AD9088 only).
        samples: The number of samples to capture.
        plot: Enable plotting.
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
    for key, value in kwargs.items():
        print(f"Setting {key} to {value}")
        if not hasattr(device, key):
            raise AttributeError(f"Device does not have attribute: {key}")
        setattr(device, key, value)

    # Capture data
    device._rxadc.set_kernel_buffers_count(1)
    device.rx_enabled_channels = [channel]
    device.rx_buffer_size = samples
    if side is None or side == "A":
        for _ in range(2):
            data = device.rx()
    elif side == "B":
        device._rxadc2.set_kernel_buffers_count(1)
        for _ in range(2):
            data = device.rx2()
    else:
        raise ValueError(f"Invalid side: {side}")

    # Write data to file
    fs, fc  = data_to_iq_datafile(device, data, filename, device_check=False)

    # Plot data
    if plot:
        import matplotlib.pyplot as plt
        from scipy import signal

        plt.figure()
        plt.plot(data.real, label="I")
        plt.plot(data.imag, label="Q")
        plt.legend()

        plt.figure()
        f, Pxx_den = signal.periodogram(data, fs)
        plt.semilogy(f, Pxx_den)
        plt.xlabel("frequency [Hz]")
        plt.ylabel("Amplitude [dBFS]")
        plt.title(f"Center Frequency: {fc}Hz")
        plt.show()

