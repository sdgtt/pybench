import logging

import pyvisa

from bench.common import Common


class SMA100A(Common):
    """Rohde & Schwarz SMA100A Signal Generator"""

    id = "SMA100A"
    """Substring returned by IDN query to identify the device"""

    def _post_init_(self, address: str = None, use_config_file=False) -> None:
        pass

    @property
    def frequency(self):
        """Get Frequency in Hz"""
        return float(self._instr.query("SOUR:FREQ:CW?"))

    @frequency.setter
    def frequency(self, value: float):
        """Set Frequency in Hz"""
        self._instr.write(f"FREQ {value}")

    @property
    def level(self):
        """Get output power level in dBm"""
        return float(self._instr.query("SOUR:POW:POW?"))

    @level.setter
    def level(self, value):
        """Set output power level in dBm"""
        self._instr.write(f"POW {value}")

    @property
    def output_enable(self):
        """Get output state"""
        return bool(self._instr.query("Output1:STATe?"))

    @output_enable.setter
    def output_enable(self, value: bool):
        """Set output state (True == On, False == Off)"""
        value = "1" if value else "0"
        self._instr.write(f"Output1:STATe {value}")
