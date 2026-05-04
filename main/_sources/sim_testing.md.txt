# Simulator-backed testing

pybench tests can run against [pyvisa-sim](https://pyvisa.readthedocs.io/projects/pyvisa-sim/) instead of real hardware. This is what CI uses to verify that every instrument class emits the SCPI it claims to.

## How it works

`bench.common.Common` accepts a `backend` argument that is passed to `pyvisa.ResourceManager`. Setting `backend="<yaml-path>@sim"` swaps the live VISA layer for pyvisa-sim, which serves canned responses out of a YAML file.

```python
from bench.keysight import N5182B

sg = N5182B(
    address="TCPIP0::sim-n5182b::inst0::INSTR",
    backend="tests/sim/keysight/n5182b.yaml@sim",
)
sg.connect()
sg.frequency = 2.4e9
assert sg.frequency == 2.4e9
```

Sim YAMLs live in `tests/sim/keysight/`. The CI workflow at `.github/workflows/test.yml` runs `tests/test_sim_keysight.py` against every YAML on push.

## Recording from real or Command Expert-emulated hardware

The `scripts/dump_to_sim.py` helper captures real SCPI traffic and writes a pyvisa-sim YAML.

The intended workflow is:

1. **Install Keysight Command Expert** (Windows). Command Expert ships with simulator personalities for most current Keysight instruments and exposes them as VISA resources on `localhost`.
2. **Configure the simulated instrument** in Command Expert so it appears at a VISA address such as `TCPIP0::127.0.0.1::INSTR`.
3. **Run the dump script** pointing at that address:

   ```sh
   python scripts/dump_to_sim.py N5182B TCPIP0::127.0.0.1::INSTR \
       --set frequency=2.4e9 \
       --set power=-10 \
       --set output_enabled=1 \
       --out tests/sim/keysight/n5182b.yaml
   ```

   The script walks every readable property on `N5182B` (skipping `reset`), then exercises any `--set name=value` setters you provide. Each captured (request, response) pair becomes a dialogue in the emitted YAML.

4. **Commit the YAML.** From here on, CI replays it via pyvisa-sim — no instrument needed.

The same script works against real hardware (drop `--backend` and use the instrument's actual VISA address), which is useful when Command Expert doesn't carry a simulator for your model.

## Limitations

- The emitted YAML uses a `dialogues` block, so query responses are frozen at capture time — writes don't update what subsequent reads return. For round-trip simulation, hand-edit the YAML to use a `properties` block (see existing files in `tests/sim/keysight/` for examples).
- Only properties defined directly on the instrument class are walked. Compound instruments with sub-objects (e.g., `E36233A.ch1`, `E36233A.ch2`) need to be dumped per sub-object or have setters supplied via `--set`.
- A passing sim test proves the SCPI string the class emits is correct, not that the instrument behaves as expected. Hardware-in-the-loop tests via the `instruments_required` pytest marker are still required for behavioral verification.
