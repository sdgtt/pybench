# Configuration

pybench instruments can be configured in two main ways. The first by providing the instrument address to the constructor of the instrument class, and the second by using a configuration file. The configuration file is a YAML file that defines the instruments available to pybench and their addresses. Using configuration files is useful when you have multiple instruments that you want to use in your tests, or if you want to keep the instrument addresses separate from your test code. pybench looks for local and global configuration files, which can be handy when you want to have multiple test code bases that use the same instruments.

## Configuration file format

The configuration file is a YAML file that defines the instruments available to pybench and their addresses. The configuration file is structured as follows:

```yaml

instrument1:
    address: "address1"
    type: "instrument_type"
instrument2:
    address: "address2"
    type: "instrument_type2"
```

Example configuration file:

```yaml
powersupply:
  address: "TCPIP0::192.168.10.31::inst0::INSTR"
  type: E36233A
specan:
  address: "TCPIP::192.168.10.21::inst0::INSTR"
  type: N9040B
siggen:
  address: "TCPIP::192.168.10.41::inst0::INSTR"
  type: SMA100A
```

The "type" field must match an instrument class in pybench. The address field is the address of the instrument, which is used to connect to the instrument. Note that the address field does not need to be TCP/IP addresses, but can be any address that the instrument class can use to connect to the instrument.