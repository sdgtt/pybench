import logging
import os
import time

import pyvisa
import yaml

common_log = logging.getLogger(__name__)


def check_connected(func):
    def check(*args, **kwargs):
        self = args[0]
        if not self._connected:
            raise Exception("Must connect to instrument first. Run connect method")
        return func(*args, **kwargs)

    return check


class instrument:
    """Shim layer between pyvisa instrument class and pybench instruments"""

    _retries = 5

    def __init__(self, rm, address, auto_reconnect=True, use_py_resource_manager=True):
        self.rm = rm
        self.address = address
        self.instr = rm.open_resource(address)
        self.auto_reconnect = auto_reconnect
        self.use_py_resource_manager = use_py_resource_manager

    def _reconnect(self, error):
        if not self.auto_reconnect:
            raise error

        print("Reconnecting")
        for retry in self._retries:
            try:
                if self.use_py_resource_manager:
                    self.rm = pyvisa.ResourceManager("@py")
                else:
                    self.rm = pyvisa.ResourceManager()
                self.instr = self.rm.open_resource(self.address)
                self.instr.timeout = 15000
                self.instr.write("*CLS")
                break
            except Exception as ex:
                print(f"Reconnect failed. Retrying {retry+1} of {self._retries}")
                time.sleep(2)
                if retry == (self._retries - 1):
                    raise ex

    def query(self, cmd):
        try:
            return self.instr.query(cmd)
        except Exception as ex:
            self._reconnect(ex)
            return self.instr.query(cmd)

    def query_ascii_values(self, cmd, converter=None):
        try:
            return self.instr.query_ascii_values(cmd, converter)
        except Exception as ex:
            self._reconnect(ex)
            return self.instr.query_ascii_values(cmd, converter)

    def write(self, cmd):
        try:
            self.instr.write(cmd)
        except Exception as ex:
            self._reconnect(ex)
            self.instr.write(cmd)

    def close(self):
        self.instr.close()

    def read_raw(self):
        try:
            return self.instr.read_raw()
        except Exception as ex:
            self._reconnect(ex)
            return self.instr.read_raw()

    @property
    def timeout(self):
        try:
            return self.instr.timeout
        except Exception as ex:
            self._reconnect(ex)
            return self.instr.timeout

    @timeout.setter
    def timeout(self, value):
        try:
            self.instr.timeout = value
        except Exception as ex:
            self._reconnect(ex)
            self.instr.timeout = value


class Common:

    config_locations = [".", "/etc/"]
    """Paths to search for config"""

    auto_connect = True
    """Automatically connect to hardware when running methods"""

    _auto_reconnect = True
    """Try to reconnect if connection dropped"""

    use_py_resource_manager = True
    """Use @py resource manager"""

    use_config_file = False
    """Use config file to get address for instrument(s)"""

    _config_file = None
    """Used config at runtime"""

    _config = None
    """Read in config"""

    _config_filename = "bench.yaml"
    """Filename used for config"""

    _connected = False
    """State of connected to instrument"""

    _teardown = False

    _retries = 5

    def __getattribute__(self, name):
        if name == "_instr":
            td = object.__getattribute__(
                self, "_teardown"
            )  # Don't trigger on destructor
            ac = object.__getattribute__(
                self, "auto_connect"
            )  # Don't trigger on destructor
            if not object.__getattribute__(self, "_connected") and not td:
                if ac:
                    self.connect()
                else:
                    raise Exception(
                        "Must connect to instrument first. Run connect method"
                    )
        return object.__getattribute__(self, name)

    @property
    def config_file(self):
        return self._config_file

    @config_file.setter
    def config_file(self, value):
        if not os.path.isfile(value):
            raise Exception(f"No config file found at {value}")
        self._config_file = value

    @property
    def auto_reconnect(self):
        """Automatically reconnect if connection dropped"""
        return self._auto_reconnect

    @auto_reconnect.setter
    def auto_reconnect(self, value):
        if hasattr(self, "_instr"):
            self._instr.auto_reconnect = value
        self._auto_reconnect = value

    def __init__(self, address: str = None, use_config_file=False) -> None:
        """Initialize the N9040B UXA

        Parameters
        ----------
        address : str, optional
            VISA address of the device. If not provided, the device will be found automatically.
        """
        if use_config_file:
            self.use_config_file = use_config_file
            self._read_from_config()
        else:
            self.address = address

        self._post_init_()

    def _post_init_(self):
        pass

    def __del__(self):
        """Close the instrument on object deletion"""
        self._teardown = True
        if hasattr(self, "_instr") and self._instr:
            self._instr.close()
        self.address = None
        if hasattr(self, "_rm") and self._rm:
            self._rm.close()

    def connect(self):
        if self._connected:
            print("Already connected")
            return
        if not self.address:
            self._find_device()
        else:
            common_log.info(f"Using address {self.address}")
            for retry in range(self._retries):
                try:
                    if self.use_py_resource_manager:
                        self._rm = pyvisa.ResourceManager("@py")
                    else:
                        self._rm = pyvisa.ResourceManager()
                    self._instr = instrument(
                        self._rm,
                        self.address,
                        self.auto_reconnect,
                        self.use_py_resource_manager,
                    )
                    break
                except Exception as ex:
                    common_log.warning(ex)
                    common_log.info(f"Retrying {retry+1}")
                    time.sleep(2)
                    if retry == (self._retries - 1):
                        raise ex
            self._connected = True
            self._instr.timeout = 15000
            self._instr.write("*CLS")
            q_id = self._instr.query("*IDN?")
            if self.id not in q_id:
                raise Exception(
                    f"Device at {self.address} is not a {self.id}. Got {q_id}"
                )

    def disconnect(self):
        if not self._connected:
            print("Not connected. Not doing anything")
            return
        self._instr.close()
        self._instr = None
        self._rm.close()
        self._rm = None

    def _find_dev_ind(self, rm):
        all_resources = rm.list_resources()
        for res in all_resources:
            common_log.info(f"Inspecting: {res}")
            idn = rm.open_resource(res).query("*IDN?")
            common_log.info(f"Found ID: {idn}")
            if self.id in idn:
                common_log.info(f"Found {self.id} at {res}")
                self.address = res
                # self._instr = rm.open_resource(self.address)
                self._instr = instrument(
                    rm, self.address, self.auto_reconnect, self.use_py_resource_manager
                )
                self._instr.timeout = 15000
                self._instr.write("*CLS")
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

    def _read_from_config(self):

        if not self._config_file:
            self._find_config()

        with open(self._config_file, "r") as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)

        for device in self._config:
            item = self._config[device]
            if "type" not in item.keys():
                print(f"{item} has no field type. Skipping ...")
                continue
            if item["type"] == self.id:
                if "address" not in item.keys():
                    print(f"{item} has no field address. Skipping ...")
                    continue
                self.address = item["address"]
                return
        raise Exception(f"No instruments of ID {self.id} found in config")

    def _find_config(self):
        """Find config on path"""
        for path in self.config_locations:
            fn = os.path.join(path, self._config_filename)
            if os.path.isfile(fn):
                self._config_file = fn
                return
        raise Exception("No config found")

    def query_error(self):
        """Queries for PXA error

        :raises AttributeError: Error
        """
        err = self._instr.query_ascii_values("SYST:ERR?", converter="s")
        err = int(err[0]), err[1]
        if err[0] != 0:
            self._inst.write("*CLS")
            print(f"ErrorCode:{err[0]}, Message:{err[1]}")
            raise AttributeError(err)
