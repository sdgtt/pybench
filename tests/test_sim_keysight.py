"""Round-trip tests for Keysight instruments against pyvisa-sim.

Each parametrized case constructs the instrument class with a sim backend,
connects (which validates that the simulated *IDN? matches the class's `id`),
and round-trips one or more primary properties.

These tests verify the SCPI strings emitted by each class and their response
parsing. They do not validate instrument behavior — that needs hardware.
"""

import os

import pytest

from bench import keysight

SIM_DIR = os.path.join(os.path.dirname(__file__), "sim", "keysight")


def _backend(yaml_name: str) -> str:
    return f"{os.path.join(SIM_DIR, yaml_name)}@sim"


@pytest.fixture
def n5182b():
    sg = keysight.N5182B(
        address="TCPIP0::sim-n5182b::inst0::INSTR", backend=_backend("n5182b.yaml")
    )
    sg.connect()
    yield sg
    sg.disconnect()


@pytest.fixture
def e8257d():
    sg = keysight.E8257D(
        address="TCPIP0::sim-e8257d::inst0::INSTR", backend=_backend("e8257d.yaml")
    )
    sg.connect()
    yield sg
    sg.disconnect()


@pytest.fixture
def n9020b():
    sa = keysight.N9020B(
        address="TCPIP0::sim-n9020b::inst0::INSTR", backend=_backend("n9020b.yaml")
    )
    sa.connect()
    yield sa
    sa.disconnect()


@pytest.fixture
def n9030b():
    sa = keysight.N9030B(
        address="TCPIP0::sim-n9030b::inst0::INSTR", backend=_backend("n9030b.yaml")
    )
    sa.connect()
    yield sa
    sa.disconnect()


@pytest.fixture
def n9040b():
    sa = keysight.N9040B(
        address="TCPIP0::sim-n9040b::inst0::INSTR", backend=_backend("n9040b.yaml")
    )
    sa.connect()
    yield sa
    sa.disconnect()


@pytest.fixture
def n5232a():
    na = keysight.N5232A(
        address="TCPIP0::sim-n5232a::inst0::INSTR", backend=_backend("n5232a.yaml")
    )
    na.connect()
    yield na
    na.disconnect()


@pytest.fixture
def e5071c():
    na = keysight.E5071C(
        address="TCPIP0::sim-e5071c::inst0::INSTR", backend=_backend("e5071c.yaml")
    )
    na.connect()
    yield na
    na.disconnect()


@pytest.fixture
def e36233a():
    ps = keysight.E36233A(
        address="TCPIP0::sim-e36233a::inst0::INSTR", backend=_backend("e36233a.yaml")
    )
    ps.connect()
    yield ps
    ps.disconnect()


def test_n5182b_roundtrip(n5182b):
    n5182b.frequency = 2.4e9
    assert n5182b.frequency == pytest.approx(2.4e9)
    n5182b.power = -5.0
    assert n5182b.power == pytest.approx(-5.0)
    n5182b.output_enabled = True
    assert n5182b.output_enabled is True
    n5182b.modulation_enabled = False
    assert n5182b.modulation_enabled is False


def test_e8257d_roundtrip(e8257d):
    e8257d.frequency = 10.0e9
    assert e8257d.frequency == pytest.approx(10.0e9)
    e8257d.power = 0.0
    assert e8257d.power == pytest.approx(0.0)
    e8257d.output_enabled = True
    assert e8257d.output_enabled is True


def test_n9020b_roundtrip(n9020b):
    n9020b.center_frequency = 2.45e9
    assert n9020b.center_frequency == pytest.approx(2.45e9)
    n9020b.span = 100e6
    assert n9020b.span == pytest.approx(100e6)
    n9020b.reference_level = -10.0
    assert n9020b.reference_level == pytest.approx(-10.0)
    n9020b.peak_search_marker(1)
    assert n9020b.get_marker_amplitude(1) == pytest.approx(-12.34)


def test_n9030b_roundtrip(n9030b):
    n9030b.center_frequency = 5.0e9
    assert n9030b.center_frequency == pytest.approx(5.0e9)
    n9030b.span = 1e9
    assert n9030b.span == pytest.approx(1e9)
    n9030b.reference_level = 0.0
    assert n9030b.reference_level == pytest.approx(0.0)


def test_n9040b_roundtrip(n9040b):
    n9040b.center_frequency = 28.0e9
    assert n9040b.center_frequency == pytest.approx(28.0e9)
    n9040b.span = 500e6
    assert n9040b.span == pytest.approx(500e6)
    n9040b.peak_search_marker(1)
    assert n9040b.get_marker_amplitude(1) == pytest.approx(-30.10)


def test_n5232a_roundtrip(n5232a):
    n5232a.start_frequency = 1e9
    assert n5232a.start_frequency == pytest.approx(1e9)
    n5232a.stop_frequency = 6e9
    assert n5232a.stop_frequency == pytest.approx(6e9)
    n5232a.num_points = 401
    assert n5232a.num_points == 401
    n5232a.output_power = -10.0
    assert n5232a.output_power == pytest.approx(-10.0)
    n5232a.output_enabled = True
    assert n5232a.output_enabled is True


def test_e5071c_roundtrip(e5071c):
    e5071c.start_frequency = 100e6
    assert e5071c.start_frequency == pytest.approx(100e6)
    e5071c.stop_frequency = 3e9
    assert e5071c.stop_frequency == pytest.approx(3e9)
    e5071c.num_points = 1601
    assert e5071c.num_points == 1601
    e5071c.output_power = -20.0
    assert e5071c.output_power == pytest.approx(-20.0)


def test_e36233a_channel_roundtrip(e36233a):
    e36233a.ch1.voltage = 5.0
    assert e36233a.ch1.voltage == pytest.approx(5.0)
    e36233a.ch2.current = 0.5
    assert e36233a.ch2.current == pytest.approx(0.5)
    e36233a.ch1.output_enabled = True
    assert e36233a.ch1.output_enabled is True
    assert e36233a.ch1.operational_mode == "OFF"
    assert e36233a.ch1.current_draw == pytest.approx(1.2345)
