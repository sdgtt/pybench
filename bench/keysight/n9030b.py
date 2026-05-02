from bench.common import Common


class N9030B(Common):
    """Keysight N9030B PXA signal analyzer."""

    id = "N9030B"
    """Substring returned by IDN query to identify the device"""

    _markers = [*range(1, 12 + 1)]

    @property
    def reset(self):
        """Reset the instrument"""
        self._instr.write("*RST")

    @property
    def center_frequency(self) -> float:
        """Center frequency in Hz"""
        return float(self._instr.query(":FREQ:CENT?"))

    @center_frequency.setter
    def center_frequency(self, value: float):
        self._instr.write(f":FREQ:CENT {value}")

    @property
    def span(self) -> float:
        """Span in Hz"""
        return float(self._instr.query(":FREQ:SPAN?"))

    @span.setter
    def span(self, value: float):
        self._instr.write(f":FREQ:SPAN {value}")

    @property
    def reference_level(self) -> float:
        """Reference level in dBm"""
        return float(self._instr.query(":DISP:WIND:TRAC:Y:RLEV?"))

    @reference_level.setter
    def reference_level(self, value: float):
        self._instr.write(f":DISP:WIND:TRAC:Y:RLEV {value}")

    def peak_search_marker(self, marker: int = 1):
        """Move marker to the maximum peak."""
        if marker not in self._markers:
            raise Exception(f"Valid markers are: {self._markers}")
        self._instr.write(f":CALC:MARK{marker}:MAX")

    def get_marker_amplitude(self, marker: int = 1) -> float:
        """Read marker Y value (dBm)."""
        if marker not in self._markers:
            raise Exception(f"Valid markers are: {self._markers}")
        return float(self._instr.query(f":CALC:MARK{marker}:Y?"))
