"""pytest plugin for pybenc"""
import os
import yaml
import logging

import pytest

import bench
from bench.common import Common as bcom

p_logger = logging.getLogger("PYBENCH-PLUGGIN")
# p_logger.setLevel(logging.INFO)

def pytest_addoption(parser):
    group = parser.getgroup("pybench")
    group.addoption(
        "--configfile",
        action="store",
        dest="configfile",
        default=None,
        help="Set location of pybench config file",
    )

@pytest.fixture(scope="session")
def parse_instruments(request):
    configfile = request.config.getoption("--configfile")

    bc = bcom()
    if not configfile:
        bc._find_config()
        configfile = bc._config_file

    if not os.path.isfile(configfile):
        raise Exception(f"pybench config file not found at {configfile}")

    # Check status of each instrument
    with open(configfile, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    valid_instruments = {}

    for device in config:
        item = config[device]
        if "type" not in item.keys():
            print(f"{item} has no field type. Skipping ...")
            continue
        if "address" not in item.keys():
            print(f"{item} has no field address. Skipping ...")
            continue
        p_logger.info(f'Trying {item["type"]} at {item["address"]}')
        try:
            dev = eval(f'''bench.all.{item["type"]}(address='{item["address"]}')''')
            dev.connect()
            valid_instruments[item["type"]] = item["address"]
            dev.disconnect()
        except Exception as ex:
            p_logger.info(f"Failed to connect to {device}")
            p_logger.info(ex)
            continue

    return valid_instruments

def _instrument_addresses(request, parse_instruments):
    print(dir(request))
    marker = request.node.get_closest_marker("instruments_required")
    if hasattr(marker, "args") and len(marker.args):
        requested = marker.args[0]
        if not isinstance(requested, list):
            requested = [requested]
        applicable = []
        # Check for requested instruments and filter out unnecessary ones
        for requested_instrument in requested:
            p_logger.info(f"Looking for {requested_instrument}")
            if requested_instrument in parse_instruments.keys():
                applicable.append({requested_instrument: parse_instruments[requested_instrument]})
            else:
                pytest.skip(f"Required Instrument not found ({requested_instrument}). Skipping...")
        return applicable
    return None

@pytest.fixture(scope="function")
def instrument_addresses(request, parse_instruments) -> dict:
    return _instrument_addresses(request, parse_instruments)

@pytest.fixture(scope="session")
def instrument_addresses_session(request, parse_instruments) -> dict:
    print("instrument_addresses_session")
    print(request.param)
    return _instrument_addresses(request, parse_instruments)
