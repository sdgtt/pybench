import logging

import pyvisa
from bench.common import Common

hmct2220_logger = logging.getLogger(__name__)


class HMCT2220(Common):

    id = "Hittite,HMC-T2220"

    def __init__(self, visa_address=None):

        if visa_address is None:
            self._find_device()
        else:
            self.address = visa_address
            self._instr = pyvisa.ResourceManager().open_resource(visa_address)
            if self.id in self._instr.query("*IDN?"):
                hmct2220_logger.debug(f"IDN: {self._instr.query('*IDN?')}")
                raise Exception(f"Device at {visa_address} is not a Hittite HMCT2220")

    @property
    def frequency(self):
        return int(self._instr.query("FREQ?"))

    @frequency.setter
    def frequency(self, freq):
        """Set frequency in MHz"""
        self._instr.write("FREQ {} MHz".format(freq))

    @property
    def power_level_dBm(self):
        """Get power level in dBm"""
        return float(self._instr.query("SOUR:POW?"))

    @power_level_dBm.setter
    def power_level_dBm(self, power_level):
        """Set power level in dBm"""
        self._instr.write("SOUR:POW {}".format(power_level))

    @property
    def output_enabled(self):
        """Get output state ON or OFF"""
        return self._instr.query("OUTP?")

    @output_enabled.setter
    def output_enabled(self, state):
        """Set output state ON or OFF"""
        state = "ON" if state else "OFF"
        self._instr.write("OUTP {}".format(state))
