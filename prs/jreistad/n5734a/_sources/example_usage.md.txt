# Usage Model

All supported instruments within pybench have a similar API and usage model. This allows for a consistent experience when using different instruments in your tests. This page describes the usage model for pybench instruments through examples.

## Basic usage

The following example demonstrates how to use a power supply instrument to set the output voltage and current, and then enable the output.

```python
from bench.keysight import E36233A

# Create an instance of the power supply
ps = E36233A("TCPIP0::192.168.1.1::inst0::INSTR")

# Set the output voltage to 5V for channel 1
ps.ch1.voltage = 5

# Set the output current to 1A for channel 2
ps.ch2.current = 1

# Enable the output for channel 1
ps.ch1.output_enabled = True

# Check output operational mode
print(ps.ch1.operational_mode)
```

## Using configuration files

The following example demonstrates how to use a configuration file to define the instruments available to pybench.

We will use the following configuration file ("bench.yaml") to define the instruments available to pybench:
```yaml
siggen:
  address: "TCPIP::192.168.1.2::inst0::INSTR"
  type: SMA100A
```

Next we will use the configuration file to create an instance of the signal generator instrument. By default pybench will look in the local directory for the configuration file. If the configuration file is not found, pybench will look in the global configuration directory based on the class property *config_locations*.
```python
siggen = SMA100A.from_config(use_config_file=True)

# Set the frequency to 1 GHz
siggen.frequency = 1e9

# Set the output power to -10 dBm
siggen.level = -10

# Enable the output
siggen.output_enable = True
```
