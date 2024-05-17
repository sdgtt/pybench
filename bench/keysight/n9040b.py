import logging
import time
import os
from typing import Union

import pyvisa

from bench.common import Common


class N9040B(Common):
    """Keysight N9040B UXA"""

    id = "N9040B"
    """Substring returned by IDN query to identify the device"""

    _markers = [*range(1,12+1)]

    def peak_search_marker(self, marker=1):
        """Set max peak search for a specific marker"""
        if marker not in self._markers:
            raise Exception(f"Valid markers are: {self._markers}")
        self._instr.write(f"CALC:MARK{marker}:MAX")

    def get_marker_amplitude(self, marker=1):
        """Get current value of marker in dBm"""
        if marker not in self._markers:
            raise Exception(f"Valid markers are: {self._markers}")
        return float(self._instr.query(f"CALC:MARK{marker}:Y?"))

    @property
    def reset(self):
        """Reset the instrument"""
        self._instr.write("*RST")

    @property
    def span(self) -> float:
        """Returns the Span in HZ"""
        return float(self._instr.query("FREQ:SPAN?"))
        
    @span.setter
    def span(self, value: float):
        """Sets the span in Hz"""
        self._instr.write("FREQ:SPAN "+str(value))

    @property
    def center_frequency(self) -> float:
        """Returns the current center frequency in Hz"""
        return float(self._instr.query("FREQ:CENT?"))
        
    @center_frequency.setter
    def center_frequency(self, value: Union[str, float]):
        """Sets the center frequency in Hz"""
        self._instr.write("FREQ:CENT "+str(value))

    def screenshot(self, filename: str = "N9040B_sc.png"):
        """Takes a screenshot on PXA and returns it locally

        Args:
            filename (str): filename+path to screenshot
        """
        path = os.path.dirname(filename)
        if path:
            if not os.path.isdir(path):
                os.mkdir(path)

        if '.png' not in filename:
            filename = f'{filename}.png'

        just_filename = os.path.basename(filename)
        self._instr.write(f':MMEM:STOR:SCR "D:\\{just_filename}"')
        self.query_error()
        time.sleep(0.5)
        self._instr.write(f':MMEM:DATA? "D:\\{just_filename}"')
        data = self._instr.read_raw()
        # Extract PNG data
        start = data.index(b'PNG') - 1
        data = data[start:]
        with open(filename, 'wb') as f:
            f.write(data)
        print(f"Wrote file: {filename}")