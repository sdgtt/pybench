import logging

import pyvisa

from bench.common import Common, check_connected


class N5734A(Common):
    """Keysight N5734A Power Supply"""

    id = "N5734A"
    """Substring returned by IDN query to identify the device"""

    @property
    def reset(self):
        """Reset the instrument"""
        self._instr.write("*RST")

    def _to_float(self, value):
        numbers = value.split("E")
        return float(numbers[0]) * pow(10, int(numbers[1]))

    @property
    @check_connected
    def voltage(self):
        """Get or set the voltage"""
        v_temp = self._instr.query("SOUR:VOLT?")
        return self._to_float(v_temp)

    @voltage.setter
    def voltage(self, value):
        self._instr.write(f"SOUR:VOLT {value}")

    @property
    def current(self):
        """Get or set the current"""
        i_temp = self._instr.query("SOUR:CURR?")
        return self._to_float(i_temp)

    @current.setter
    def current(self, value):
        self._instr.write(f"SOUR:CURR {value}")

    @property
    def output_enabled(self):
        """Enable output (True) or disable output (False)"""
        return bool(self._instr.query("OUTP:STAT?") == "1")

    @output_enabled.setter
    def output_enabled(self, value) -> bool:
        value = 1 if value else 0
        self._instr.write(f"OUTP:STAT {value}")

    @property
    def current_draw(self):
        """Get the current draw"""
        i_temp = self._instr.query("MEAS:CURR:DC?")
        return self._to_float(i_temp)