import pyvisa

import logging

from bench.common import Common

hmct2220_logger = logging.basicConfig(level=logging.DEBUG)

class HMCT2220(Common):

    id = "Hittite,HMCT2220,0,1.0"

    def __init__(self, visa_address=None):

        if visa_address is None:
            self._find_device()
        else:
            self.address = visa_address
            self._instr = pyvisa.ResourceManager().open_resource(visa_address)
            if self._instr.query("*IDN?") != self.id:
                hmct2220_logger.debug(f"IDN: {self._instr.query('*IDN?')}")
                raise Exception(f"Device at {visa_address} is not a Hittite HMCT2220")


        # self._instr = pyvisa.ResourceManager().open_resource(visa_address)
        # self._instr.write_termination = "\n"
        # self._instr.read_termination = "\n"
        # self._instr.write("*CLS")
        # self._instr.write("SYST:REM")
        # self._instr.write("SYST:RWL OFF")
        # self._instr.write("SYST:ZCH OFF")
        # self._instr.write("SYST:ZCOR OFF")
        # self._instr.write("SYST:ZCH OFF")
        # self._instr.write("SYST:ZCOR