import logging

import pyvisa

from bench.common import Common, check_connected


class channel:
    """Individual output channel on the E36233A power supply
    """

    def __init__(self, parent, channel_number):
        self.parent = parent
        self.channel_number = channel_number

    @property
    def _connected(self):
        return self.parent._connected

    def _set_channel(self):
        self.parent._instr.write(f"INST CH{self.channel_number}")

    def _to_float(self, value):
        numbers = value.split("E")
        return float(numbers[0]) * pow(10, int(numbers[1]))

    @property
    @check_connected
    def voltage(self):
        """Get or set the voltage of the channel"""
        self._set_channel()
        v_temp = self.parent._instr.query("SOUR:VOLT?")
        return self._to_float(v_temp)

    @voltage.setter
    def voltage(self, value):
        """Get or set the voltage of the channel"""
        self._set_channel()
        self.parent._instr.write(f"SOUR:VOLT {value}")

    @property
    def current(self):
        """Get or set the current of the channel"""
        self._set_channel()
        i_temp = self.parent._instr.query("SOUR:CURR?")
        return self._to_float(i_temp)

    @current.setter
    def current(self, value):
        self._set_channel()
        self.parent._instr.write(f"SOUR:CURR {value}")

    @property
    def output_enabled(self):
        """Enable output of channel (True) or disable output (False)"""
        self._set_channel()
        return bool(self.parent._instr.query("OUTP:STAT?") == "1")

    @output_enabled.setter
    def output_enabled(self, value) -> bool:
        self._set_channel()
        value = 1 if value else 0
        self.parent._instr.write(f"OUTP:STAT {value}")

    @property
    def operational_mode(self) -> str:
        """Get or set the operational mode of the channel. Options are:
        OFF: Channel is off
        SER: Channel is in series mode
        PAR: Channel is in parallel mode
        """
        self._set_channel()
        return str(self.parent._instr.query("OUTP:PAIR?")).replace("\n", "")

    @operational_mode.setter
    def operational_mode(self, value: str):
        self._set_channel()
        if value not in ["OFF", "SER", "PAR"]:
            raise Exception("Invalid operational mode. Must be one of: OFF, SER, PAR")
        self.parent._instr.write(f"OUTP:PAIR {value}")

    @property
    def current_draw(self):
        """Get the current draw of the channel"""
        self._set_channel()
        i_temp = self.parent._instr.query("MEASure:SCALar:CURRent:DC?")
        return self._to_float(i_temp)


class E36233A(Common):
    """Keysight E36233A Power Supply"""

    id = "E36233A"
    """Substring returned by IDN query to identify the device"""

    num_channels = 2
    """Number of channels on the device"""

    def _post_init_(self, address: str = None, use_config_file=False) -> None:
        self.ch1 = channel(self, 1)
        self.ch2 = channel(self, 2)

    def channels(self):
        """List all channels"""
        return [self.ch1, self.ch2]

    @property
    def reset(self):
        """Reset the instrument"""
        self._instr.write("*RST")
