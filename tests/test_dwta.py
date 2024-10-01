"""Test the DWTA class."""

import os
import pytest
import adi
import bench

hardware = ["pluto", "pluto_rev_c"]

loc = os.path.dirname(os.path.realpath(__file__))
ref_data_folder = os.path.join(loc, "ref_data")


@pytest.mark.iio_hardware(hardware)
def test_iq_datafile_gen(iio_uri, tmpdir):
    """Test the IQ datafile generation."""
    dev = adi.Pluto(iio_uri)
    dev.rx_buffer_size = 2**10
    data = dev.rx()

    filename = tmpdir.join("test_iq.csv")
    d = bench.keysight.dwta.utils.data_to_iq_datafile(
        dev, data, tmpdir.join("test_iq.csv")
    )

    # Check structure
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0
    with open(filename, "r") as f:
        lines = f.readlines()
        assert len(lines) == dev.rx_buffer_size + 2
        assert lines[0] == f"SampleRate={dev.sample_rate}\n"
        assert lines[1] == f"CenterFrequency={dev.rx_lo}\n"
