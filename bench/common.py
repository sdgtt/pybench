import pyvisa

import logging

common_log = logging.basicConfig(level=logging.DEBUG)


class Common:
    def _find_device(self):
        """Find desired devices automatically"""

        rm = pyvisa.ResourceManager()
        all_resources = rm.list_resources()
        for res in all_resources:
            common_log.debug(f"Inspecting: {res}")
            idn = rm.open_resource(res).query("*IDN?")
            common_log.debug(f"Found ID: {idn}")
            if idn == self.id:
                self.address = res
                self._instr = rm.open_resource(self.address)
                return
        raise Exception(f"No instrument found with ID: {self.id}")
