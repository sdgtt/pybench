from bench.common import Common


class N5182B(Common):
    """Keysight N5182B MXG vector signal generator (9 kHz - 6 GHz)."""

    id = "N5182B"
    """Substring returned by IDN query to identify the device"""

    @property
    def reset(self):
        """Reset the instrument"""
        self._instr.write("*RST")

    @property
    def frequency(self) -> float:
        """RF carrier frequency in Hz"""
        return float(self._instr.query(":FREQ?"))

    @frequency.setter
    def frequency(self, value: float):
        self._instr.write(f":FREQ {value}")

    @property
    def power(self) -> float:
        """Output power level in dBm"""
        return float(self._instr.query(":POW?"))

    @power.setter
    def power(self, value: float):
        self._instr.write(f":POW {value}")

    @property
    def output_enabled(self) -> bool:
        """RF output state"""
        return bool(int(self._instr.query(":OUTP?")))

    @output_enabled.setter
    def output_enabled(self, value: bool):
        self._instr.write(f":OUTP {1 if value else 0}")

    @property
    def modulation_enabled(self) -> bool:
        """Modulation source on/off"""
        return bool(int(self._instr.query(":OUTP:MOD?")))

    @modulation_enabled.setter
    def modulation_enabled(self, value: bool):
        self._instr.write(f":OUTP:MOD {1 if value else 0}")
