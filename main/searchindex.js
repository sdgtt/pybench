Search.setIndex({"docnames": ["config_file", "example_usage", "frameworks/pytest", "index", "install", "instruments/bench.common", "instruments/bench.hittite.hmct2220", "instruments/bench.keysight.e36233a", "instruments/bench.keysight.n9040b", "instruments/bench.rs.sma100a", "instruments/index"], "filenames": ["config_file.md", "example_usage.md", "frameworks/pytest.md", "index.rst", "install.md", "instruments/bench.common.rst", "instruments/bench.hittite.hmct2220.rst", "instruments/bench.keysight.e36233a.rst", "instruments/bench.keysight.n9040b.rst", "instruments/bench.rs.sma100a.rst", "instruments/index.md"], "titles": ["Configuration", "Usage Model", "pytest", "pybench: Lab Bench Instrument Controls in Python", "Installation", "bench.common module", "Hittite HMCT2220 Frequency Generator", "Keysight E36233A Power Supply", "Keysight N9040B UXA Spectrum Analyzer", "Rohde &amp; Schwarz SMA100A Signal Generator", "Supported Instruments"], "terms": {"pybench": [0, 1, 2, 4, 5], "instrument": [0, 1, 2, 4, 5, 7, 8], "can": [0, 2], "two": 0, "main": 0, "wai": 0, "The": [0, 1, 2, 3, 4], "first": 0, "provid": [0, 2, 3], "address": [0, 1, 2, 5, 7, 8, 9], "constructor": 0, "class": [0, 1, 2, 5, 6, 7, 8, 9], "second": 0, "us": [0, 2, 3, 4, 5], "i": [0, 1, 2, 3, 4, 7], "yaml": [0, 1], "defin": [0, 1, 2], "avail": [0, 1], "when": [0, 1, 4, 5], "you": [0, 4], "have": [0, 1], "multipl": 0, "want": 0, "your": [0, 1, 2], "test": [0, 1, 2, 3], "keep": 0, "separ": 0, "from": [0, 1], "code": 0, "look": [0, 1], "local": [0, 1, 8], "global": [0, 1], "which": [0, 2], "handi": 0, "base": [0, 1, 2, 5, 6, 7, 8, 9], "same": 0, "structur": 0, "follow": [0, 1, 2, 4], "instrument1": 0, "address1": 0, "type": [0, 1], "instrument_typ": 0, "instrument2": 0, "address2": 0, "instrument_type2": 0, "exampl": [0, 1], "powersuppli": 0, "tcpip0": [0, 1], "192": [0, 1], "168": [0, 1], "10": [0, 1], "31": 0, "inst0": [0, 1], "instr": [0, 1], "e36233a": [0, 1, 10], "specan": 0, "tcpip": [0, 1], "21": 0, "n9040b": [0, 10], "siggen": [0, 1], "41": 0, "sma100a": [0, 1, 10], "field": 0, "must": 0, "match": 0, "an": [0, 1, 2], "connect": [0, 5], "note": 0, "doe": 0, "need": [0, 4], "tcp": 0, "ip": 0, "ani": [0, 3], "all": [1, 2, 7], "support": [1, 3], "within": 1, "similar": 1, "api": 1, "thi": [1, 2, 3], "allow": 1, "consist": [1, 3], "experi": 1, "differ": 1, "page": [1, 3], "describ": 1, "through": 1, "demonstr": 1, "how": 1, "power": [1, 6, 9, 10], "suppli": [1, 10], "set": [1, 7, 8], "output": [1, 6, 7, 9], "voltag": [1, 7], "current": [1, 7, 8], "enabl": [1, 7], "bench": [1, 6, 7, 8, 9], "keysight": 1, "import": 1, "creat": 1, "instanc": 1, "p": 1, "1": [1, 8], "5v": 1, "channel": [1, 7], "ch1": 1, "5": [1, 8], "1a": 1, "2": [1, 7, 8], "ch2": 1, "output_en": [1, 6, 7, 9], "true": [1, 5, 7], "check": 1, "oper": [1, 7], "mode": [1, 7], "print": 1, "operational_mod": [1, 7], "we": 1, "next": 1, "signal": [1, 10], "gener": [1, 10], "By": 1, "default": [1, 2], "directori": 1, "If": [1, 2], "found": 1, "properti": [1, 5, 6, 7, 8, 9], "config_loc": [1, 5], "from_config": 1, "use_config_fil": [1, 5, 7, 8, 9], "frequenc": [1, 8, 9, 10], "ghz": 1, "1e9": 1, "dbm": [1, 6, 8, 9], "level": [1, 6, 9], "integr": 2, "either": 2, "directli": 2, "leverag": 2, "ar": [2, 4, 7], "design": [2, 3], "help": 2, "manag": [2, 5], "lifecycl": 2, "data": 2, "acquisit": 2, "process": 2, "also": [2, 3], "includ": 2, "requir": [2, 4], "make": 2, "them": 2, "interchang": 2, "what": 2, "user": 2, "ha": 2, "physic": 2, "access": 2, "confifil": 2, "path": [2, 5, 8], "configur": [2, 3], "file": [2, 4, 5], "run": [2, 4, 5], "instrument_address": 2, "A": 2, "return": [2, 7, 8, 9], "list": [2, 7], "those": 2, "specifi": 2, "instrument_address_sess": 2, "session": 2, "scope": 2, "durat": 2, "packag": 3, "It": [3, 4], "easi": 3, "interfac": 3, "wide": 3, "varieti": 3, "primarili": 3, "visa": 3, "standard": 3, "commun": [3, 4], "other": 3, "method": [3, 5], "well": 3, "modul": [3, 4], "pytest": 3, "modern": 3, "ci": 3, "driven": 3, "develop": 3, "instal": 3, "usag": 3, "model": 3, "index": 3, "search": [3, 5, 8], "endors": 3, "affili": 3, "manufactur": 3, "project": 3, "offici": 3, "compat": 4, "python": 4, "3": 4, "6": [4, 8], "abov": 4, "recommend": 4, "virtual": 4, "environ": 4, "To": 4, "command": 4, "m": 4, "venv": 4, "window": 4, "script": 4, "activ": 4, "linux": 4, "sourc": 4, "bin": 4, "pip": 4, "major": 4, "depend": 4, "via": 4, "txt": 4, "repo": 4, "howev": 4, "some": 4, "manual": 4, "certain": 4, "work": 4, "improv": 4, "function": 4, "Its": 4, "io": 4, "librari": 4, "driver": 4, "suit": 4, "download": 4, "str": [5, 7, 8, 9], "none": [5, 6, 7, 8, 9], "fals": [5, 7, 8, 9], "object": [5, 7], "auto_connect": 5, "automat": 5, "hardwar": 5, "auto_reconnect": 5, "reconnect": 5, "drop": 5, "config_fil": 5, "etc": 5, "config": 5, "disconnect": 5, "query_error": 5, "queri": [5, 7, 8, 9], "pxa": [5, 8], "error": 5, "rais": 5, "attributeerror": 5, "get": [5, 6, 7, 8, 9], "": 5, "use_py_resource_manag": 5, "py": 5, "resourc": 5, "check_connect": 5, "func": 5, "rm": 5, "shim": 5, "layer": 5, "between": 5, "pyvisa": 5, "close": 5, "cmd": 5, "query_ascii_valu": 5, "convert": 5, "read_raw": 5, "timeout": 5, "write": 5, "visa_address": 6, "common": [6, 7, 8, 9], "id": [6, 7, 8, 9], "hmc": 6, "t2220": 6, "state": [6, 9], "ON": 6, "off": [6, 7], "power_level_dbm": 6, "substr": [7, 8, 9], "idn": [7, 8, 9], "identifi": [7, 8, 9], "devic": [7, 8, 9], "num_channel": 7, "number": [7, 8], "reset": [7, 8], "parent": 7, "channel_numb": 7, "individu": 7, "option": [7, 8], "ser": 7, "seri": 7, "par": 7, "parallel": 7, "disabl": 7, "center_frequ": 8, "float": 8, "center": 8, "hz": [8, 9], "get_marker_amplitud": 8, "marker": 8, "valu": 8, "get_peak_t": 8, "peak_threshold_dbm": 8, "excursion_db": 8, "dict": 8, "tabl": 8, "peak": 8, "arg": 8, "minimum": 8, "threshold": 8, "variat": 8, "consid": 8, "measure_sfdr": 8, "span_hz": 8, "center_frequency_hz": 8, "max_iter": 8, "int": 8, "4": 8, "level_step_dbm": 8, "determin": 8, "sfdr": 8, "dbc": 8, "span": 8, "maximum": 8, "iter": 8, "least": 8, "nois": 8, "step": 8, "decreas": 8, "until": 8, "count": 8, "peak_search_mark": 8, "max": 8, "specif": 8, "peak_tabl": 8, "statu": 8, "screenshot": 8, "filenam": 8, "n9040b_sc": 8, "png": 8, "take": 8, "r": 9, "hmct2220": 10, "uxa": 10, "spectrum": 10, "analyz": 10}, "objects": {"bench": [[5, 0, 0, "-", "common"]], "bench.common": [[5, 1, 1, "", "Common"], [5, 5, 1, "", "check_connected"], [5, 1, 1, "", "instrument"]], "bench.common.Common": [[5, 2, 1, "", "auto_connect"], [5, 3, 1, "", "auto_reconnect"], [5, 3, 1, "", "config_file"], [5, 2, 1, "", "config_locations"], [5, 4, 1, "", "connect"], [5, 4, 1, "", "disconnect"], [5, 4, 1, "", "query_error"], [5, 2, 1, "", "use_config_file"], [5, 2, 1, "", "use_py_resource_manager"]], "bench.common.instrument": [[5, 4, 1, "", "close"], [5, 4, 1, "", "query"], [5, 4, 1, "", "query_ascii_values"], [5, 4, 1, "", "read_raw"], [5, 3, 1, "", "timeout"], [5, 4, 1, "", "write"]], "bench.hittite": [[6, 0, 0, "-", "hmct2220"]], "bench.hittite.hmct2220": [[6, 1, 1, "", "HMCT2220"]], "bench.hittite.hmct2220.HMCT2220": [[6, 3, 1, "", "frequency"], [6, 2, 1, "", "id"], [6, 3, 1, "", "output_enabled"], [6, 3, 1, "", "power_level_dBm"]], "bench.keysight": [[7, 0, 0, "-", "e36233a"], [8, 0, 0, "-", "n9040b"]], "bench.keysight.e36233a": [[7, 1, 1, "", "E36233A"], [7, 1, 1, "", "channel"]], "bench.keysight.e36233a.E36233A": [[7, 4, 1, "", "channels"], [7, 2, 1, "", "id"], [7, 2, 1, "", "num_channels"], [7, 3, 1, "", "reset"]], "bench.keysight.e36233a.channel": [[7, 3, 1, "", "current"], [7, 3, 1, "", "operational_mode"], [7, 3, 1, "", "output_enabled"], [7, 3, 1, "", "voltage"]], "bench.keysight.n9040b": [[8, 1, 1, "", "N9040B"]], "bench.keysight.n9040b.N9040B": [[8, 3, 1, "", "center_frequency"], [8, 4, 1, "", "get_marker_amplitude"], [8, 4, 1, "", "get_peak_table"], [8, 2, 1, "", "id"], [8, 4, 1, "", "measure_sfdr"], [8, 4, 1, "", "peak_search_marker"], [8, 3, 1, "", "peak_table"], [8, 3, 1, "", "reset"], [8, 4, 1, "", "screenshot"], [8, 3, 1, "", "span"]], "bench.rs": [[9, 0, 0, "-", "sma100a"]], "bench.rs.sma100a": [[9, 1, 1, "", "SMA100A"]], "bench.rs.sma100a.SMA100A": [[9, 3, 1, "", "frequency"], [9, 2, 1, "", "id"], [9, 3, 1, "", "level"], [9, 3, 1, "", "output_enable"]]}, "objtypes": {"0": "py:module", "1": "py:class", "2": "py:attribute", "3": "py:property", "4": "py:method", "5": "py:function"}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "class", "Python class"], "2": ["py", "attribute", "Python attribute"], "3": ["py", "property", "Python property"], "4": ["py", "method", "Python method"], "5": ["py", "function", "Python function"]}, "titleterms": {"configur": [0, 1], "file": [0, 1], "format": 0, "usag": 1, "model": 1, "basic": 1, "us": 1, "pytest": 2, "cli": 2, "option": 2, "avail": 2, "fixtur": 2, "pybench": 3, "lab": 3, "bench": [3, 5], "instrument": [3, 10], "control": 3, "python": 3, "user": 3, "guid": 3, "framework": 3, "special": 3, "function": 3, "indic": 3, "tabl": 3, "disclaim": 3, "instal": 4, "keysight": [4, 7, 8, 10], "common": 5, "modul": 5, "hittit": [6, 10], "hmct2220": 6, "frequenc": 6, "gener": [6, 9], "e36233a": 7, "power": 7, "suppli": 7, "n9040b": 8, "uxa": 8, "spectrum": 8, "analyz": 8, "rohd": [9, 10], "schwarz": [9, 10], "sma100a": 9, "signal": 9, "support": 10}, "envversion": {"sphinx.domains.c": 3, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 9, "sphinx.domains.index": 1, "sphinx.domains.javascript": 3, "sphinx.domains.math": 2, "sphinx.domains.python": 4, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx": 58}, "alltitles": {"Configuration": [[0, "configuration"]], "Configuration file format": [[0, "configuration-file-format"]], "Usage Model": [[1, "usage-model"]], "Basic usage": [[1, "basic-usage"]], "Using configuration files": [[1, "using-configuration-files"]], "pytest": [[2, "pytest"]], "CLI options": [[2, "cli-options"]], "Available fixtures": [[2, "available-fixtures"]], "pybench: Lab Bench Instrument Controls in Python": [[3, "pybench-lab-bench-instrument-controls-in-python"]], "User Guide": [[3, null]], "Frameworks": [[3, null]], "Special Functionality": [[3, null]], "Indices and tables": [[3, "indices-and-tables"]], "Disclaimer": [[3, "disclaimer"]], "Installation": [[4, "installation"]], "Keysight": [[4, "keysight"], [10, null]], "bench.common module": [[5, "module-bench.common"]], "Hittite HMCT2220 Frequency Generator": [[6, "module-bench.hittite.hmct2220"]], "Keysight E36233A Power Supply": [[7, "module-bench.keysight.e36233a"]], "Keysight N9040B UXA Spectrum Analyzer": [[8, "module-bench.keysight.n9040b"]], "Rohde & Schwarz SMA100A Signal Generator": [[9, "module-bench.rs.sma100a"]], "Supported Instruments": [[10, "supported-instruments"]], "Hittite": [[10, null]], "Rohde & Schwarz": [[10, null]]}, "indexentries": {"common (class in bench.common)": [[5, "bench.common.Common"]], "auto_connect (bench.common.common attribute)": [[5, "bench.common.Common.auto_connect"]], "auto_reconnect (bench.common.common property)": [[5, "bench.common.Common.auto_reconnect"]], "bench.common": [[5, "module-bench.common"]], "check_connected() (in module bench.common)": [[5, "bench.common.check_connected"]], "close() (bench.common.instrument method)": [[5, "bench.common.instrument.close"]], "config_file (bench.common.common property)": [[5, "bench.common.Common.config_file"]], "config_locations (bench.common.common attribute)": [[5, "bench.common.Common.config_locations"]], "connect() (bench.common.common method)": [[5, "bench.common.Common.connect"]], "disconnect() (bench.common.common method)": [[5, "bench.common.Common.disconnect"]], "instrument (class in bench.common)": [[5, "bench.common.instrument"]], "module": [[5, "module-bench.common"], [6, "module-bench.hittite.hmct2220"], [7, "module-bench.keysight.e36233a"], [8, "module-bench.keysight.n9040b"], [9, "module-bench.rs.sma100a"]], "query() (bench.common.instrument method)": [[5, "bench.common.instrument.query"]], "query_ascii_values() (bench.common.instrument method)": [[5, "bench.common.instrument.query_ascii_values"]], "query_error() (bench.common.common method)": [[5, "bench.common.Common.query_error"]], "read_raw() (bench.common.instrument method)": [[5, "bench.common.instrument.read_raw"]], "timeout (bench.common.instrument property)": [[5, "bench.common.instrument.timeout"]], "use_config_file (bench.common.common attribute)": [[5, "bench.common.Common.use_config_file"]], "use_py_resource_manager (bench.common.common attribute)": [[5, "bench.common.Common.use_py_resource_manager"]], "write() (bench.common.instrument method)": [[5, "bench.common.instrument.write"]], "hmct2220 (class in bench.hittite.hmct2220)": [[6, "bench.hittite.hmct2220.HMCT2220"]], "bench.hittite.hmct2220": [[6, "module-bench.hittite.hmct2220"]], "frequency (bench.hittite.hmct2220.hmct2220 property)": [[6, "bench.hittite.hmct2220.HMCT2220.frequency"]], "id (bench.hittite.hmct2220.hmct2220 attribute)": [[6, "bench.hittite.hmct2220.HMCT2220.id"]], "output_enabled (bench.hittite.hmct2220.hmct2220 property)": [[6, "bench.hittite.hmct2220.HMCT2220.output_enabled"]], "power_level_dbm (bench.hittite.hmct2220.hmct2220 property)": [[6, "bench.hittite.hmct2220.HMCT2220.power_level_dBm"]], "e36233a (class in bench.keysight.e36233a)": [[7, "bench.keysight.e36233a.E36233A"]], "bench.keysight.e36233a": [[7, "module-bench.keysight.e36233a"]], "channel (class in bench.keysight.e36233a)": [[7, "bench.keysight.e36233a.channel"]], "channels() (bench.keysight.e36233a.e36233a method)": [[7, "bench.keysight.e36233a.E36233A.channels"]], "current (bench.keysight.e36233a.channel property)": [[7, "bench.keysight.e36233a.channel.current"]], "id (bench.keysight.e36233a.e36233a attribute)": [[7, "bench.keysight.e36233a.E36233A.id"]], "num_channels (bench.keysight.e36233a.e36233a attribute)": [[7, "bench.keysight.e36233a.E36233A.num_channels"]], "operational_mode (bench.keysight.e36233a.channel property)": [[7, "bench.keysight.e36233a.channel.operational_mode"]], "output_enabled (bench.keysight.e36233a.channel property)": [[7, "bench.keysight.e36233a.channel.output_enabled"]], "reset (bench.keysight.e36233a.e36233a property)": [[7, "bench.keysight.e36233a.E36233A.reset"]], "voltage (bench.keysight.e36233a.channel property)": [[7, "bench.keysight.e36233a.channel.voltage"]], "n9040b (class in bench.keysight.n9040b)": [[8, "bench.keysight.n9040b.N9040B"]], "bench.keysight.n9040b": [[8, "module-bench.keysight.n9040b"]], "center_frequency (bench.keysight.n9040b.n9040b property)": [[8, "bench.keysight.n9040b.N9040B.center_frequency"]], "get_marker_amplitude() (bench.keysight.n9040b.n9040b method)": [[8, "bench.keysight.n9040b.N9040B.get_marker_amplitude"]], "get_peak_table() (bench.keysight.n9040b.n9040b method)": [[8, "bench.keysight.n9040b.N9040B.get_peak_table"]], "id (bench.keysight.n9040b.n9040b attribute)": [[8, "bench.keysight.n9040b.N9040B.id"]], "measure_sfdr() (bench.keysight.n9040b.n9040b method)": [[8, "bench.keysight.n9040b.N9040B.measure_sfdr"]], "peak_search_marker() (bench.keysight.n9040b.n9040b method)": [[8, "bench.keysight.n9040b.N9040B.peak_search_marker"]], "peak_table (bench.keysight.n9040b.n9040b property)": [[8, "bench.keysight.n9040b.N9040B.peak_table"]], "reset (bench.keysight.n9040b.n9040b property)": [[8, "bench.keysight.n9040b.N9040B.reset"]], "screenshot() (bench.keysight.n9040b.n9040b method)": [[8, "bench.keysight.n9040b.N9040B.screenshot"]], "span (bench.keysight.n9040b.n9040b property)": [[8, "bench.keysight.n9040b.N9040B.span"]], "sma100a (class in bench.rs.sma100a)": [[9, "bench.rs.sma100a.SMA100A"]], "bench.rs.sma100a": [[9, "module-bench.rs.sma100a"]], "frequency (bench.rs.sma100a.sma100a property)": [[9, "bench.rs.sma100a.SMA100A.frequency"]], "id (bench.rs.sma100a.sma100a attribute)": [[9, "bench.rs.sma100a.SMA100A.id"]], "level (bench.rs.sma100a.sma100a property)": [[9, "bench.rs.sma100a.SMA100A.level"]], "output_enable (bench.rs.sma100a.sma100a property)": [[9, "bench.rs.sma100a.SMA100A.output_enable"]]}})