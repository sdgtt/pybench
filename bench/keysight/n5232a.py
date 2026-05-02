from bench.common import Common


class N5232A(Common):
    """Keysight N5232A PNA-L network analyzer (4-port, up to 20 GHz)."""

    id = "N5232A"
    """Substring returned by IDN query to identify the device"""

    @property
    def reset(self):
        """Reset the instrument"""
        self._instr.write("*RST")

    @property
    def start_frequency(self) -> float:
        """Sweep start frequency in Hz"""
        return float(self._instr.query(":SENS:FREQ:STAR?"))

    @start_frequency.setter
    def start_frequency(self, value: float):
        self._instr.write(f":SENS:FREQ:STAR {value}")

    @property
    def stop_frequency(self) -> float:
        """Sweep stop frequency in Hz"""
        return float(self._instr.query(":SENS:FREQ:STOP?"))

    @stop_frequency.setter
    def stop_frequency(self, value: float):
        self._instr.write(f":SENS:FREQ:STOP {value}")

    @property
    def num_points(self) -> int:
        """Number of sweep points"""
        return int(self._instr.query(":SENS:SWE:POIN?"))

    @num_points.setter
    def num_points(self, value: int):
        self._instr.write(f":SENS:SWE:POIN {int(value)}")

    @property
    def output_power(self) -> float:
        """Source output power in dBm"""
        return float(self._instr.query(":SOUR:POW?"))

    @output_power.setter
    def output_power(self, value: float):
        self._instr.write(f":SOUR:POW {value}")

    @property
    def output_enabled(self) -> bool:
        """RF output state"""
        return bool(int(self._instr.query(":OUTP?")))

    @output_enabled.setter
    def output_enabled(self, value: bool):
        self._instr.write(f":OUTP {1 if value else 0}")
