import logging
import os
import time
from typing import Union

import pyvisa

from bench.common import Common


class N9040B(Common):
    """Keysight N9040B UXA"""

    id = "N9040B"
    """Substring returned by IDN query to identify the device"""

    _markers = [*range(1, 12 + 1)]

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
        self._instr.write("FREQ:SPAN " + str(value))

    @property
    def center_frequency(self) -> float:
        """Returns the current center frequency in Hz"""
        return float(self._instr.query("FREQ:CENT?"))

    @center_frequency.setter
    def center_frequency(self, value: Union[str, float]):
        """Sets the center frequency in Hz"""
        self._instr.write("FREQ:CENT " + str(value))

    @property
    def peak_table(self):
        """Get peak table status"""
        return self._instr.query(":CALC:MARK:TABLe:STAT?")

    @peak_table.setter
    def peak_table(self, value: int):
        """Sets the peak table status"""
        self._instr.write(f":CALC:MARK:PEAK:TABLe:STAT {value}")
        self._instr.write(":CALC:MARK:PEAK:SORT FREQ")
        self._instr.write(":CALC:MARK:PEAK:TABLe:READ ALL")

    def get_peak_table(
        self, peak_threshold_dBm: float, excursion_dB: float = 5
    ) -> dict:
        """Get table of peaks

        Args:
            peak_threshold_dBm (float) : Minimum threshold for peak
            excursion_dB (float) : Minimum variation to be considered a peak
        """
        data = self._instr.query(
            f":CALCulate:DATA:PEAKs? {peak_threshold_dBm},{excursion_dB}"
        )
        data = data.split(",")
        num_peaks = data[0]
        if num_peaks == 0:
            return None
        data = data[1:]
        data = [float(d) for d in data]
        peaks = []
        for i in range(0, len(data), 2):
            peaks.append({"amplitude_dBm": data[i], "frequency_hz": data[i + 1]})
        return peaks

    def measure_sfdr(
        self,
        span_hz=None,
        center_frequency_hz=None,
        max_iterations: int = 4,
        level_step_dBm: float = 6,
    ) -> float:
        """Determine SFDR in dBc

        Args:
            span_hz (int optional): Set span in Hz
            center_frequency_hz (int optional): Set center frequency in Hz
            max_iterations (int optional): Maximum number of iterations to get at least 2 peaks
            level_step_dBm (float optional): Noise steps to decrease threshold until peak count > 1
        """
        if span_hz:
            self.span = span_hz
        if center_frequency_hz:
            self.center_frequency = center_frequency_hz
        level = -100 + level_step_dBm
        for _ in range(max_iterations):
            level = level - level_step_dBm
            peaks = self.get_peak_table(level)
            if len(peaks) >= 2:
                return peaks[0]["amplitude_dBm"] - peaks[1]["amplitude_dBm"]
        raise Exception(f"Not enough peaks found. Min level used ({level} dBm)")

    def screenshot(self, filename: str = "N9040B_sc.png"):
        """Takes a screenshot on PXA and returns it locally

        Args:
            filename (str): filename+path to screenshot
        """
        path = os.path.dirname(filename)
        if path:
            if not os.path.isdir(path):
                os.mkdir(path)

        if ".png" not in filename:
            filename = f"{filename}.png"

        just_filename = os.path.basename(filename)
        self._instr.write(f':MMEM:STOR:SCR "D:\\{just_filename}"')
        self.query_error()
        time.sleep(0.5)
        self._instr.write(f':MMEM:DATA? "D:\\{just_filename}"')
        data = self._instr.read_raw()
        # Extract PNG data
        start = data.index(b"PNG") - 1
        data = data[start:]
        with open(filename, "wb") as f:
            f.write(data)
        print(f"Wrote file: {filename}")
