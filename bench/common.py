import logging
import os

import pyvisa

common_log = logging.getLogger(__name__)


class Common:
    def __del__(self):
        """Close the instrument on object deletion"""
        self._instr.close()
        self.address = None
        self._rm.close()

    def _find_dev_ind(self, rm):
        all_resources = rm.list_resources()
        for res in all_resources:
            common_log.info(f"Inspecting: {res}")
            idn = rm.open_resource(res).query("*IDN?")
            common_log.info(f"Found ID: {idn}")
            if self.id in idn:
                common_log.info(f"Found {self.id} at {res}")
                self.address = res
                self._instr = rm.open_resource(self.address)
                return True

        return False

    def _find_device(self):
        """Find desired devices automatically"""

        if os.name != "posix":
            self._rm = pyvisa.ResourceManager()
            if self._find_dev_ind(self._rm):
                return
            self._rm.close()
            common_log.info("Using pyvisa failed, trying pyvisa-py")

        common_log.info("Trying pyvisa-py")
        self._rm = pyvisa.ResourceManager("@py")
        if self._find_dev_ind(self._rm):
            return

        raise Exception(f"No instrument found with ID: {self.id}")
