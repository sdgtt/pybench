"""Dump a real (or Command Expert-emulated) instrument to a pyvisa-sim YAML.

Connects to an instrument via a pybench class, walks every readable property
to capture SCPI queries and their responses, optionally exercises setters from
``--set name=value`` arguments, and writes a pyvisa-sim YAML containing all
captured (request, response) dialogues.

The output is "frozen": queries replay the captured response regardless of
prior writes. That's enough to let CI verify SCPI string correctness; for
true round-trip simulation, hand-edit the YAML to use a ``properties`` block.

Example
-------
    # Point Command Expert at a simulated N5182B, expose VISA at TCPIP0::127.0.0.1...
    python scripts/dump_to_sim.py N5182B TCPIP0::127.0.0.1::INSTR \\
        --set frequency=2.4e9 --set power=-10 --set output_enabled=1 \\
        --out tests/sim/keysight/n5182b.yaml
"""

import argparse
import sys
from typing import List, Tuple

from bench import all as bench_all


class Recorder:
    """Wrap pybench's ``instrument`` so every query/write is captured."""

    def __init__(self, real):
        self._real = real
        self.dialogues: List[Tuple[str, str]] = []

    def query(self, cmd):
        r = self._real.query(cmd)
        self.dialogues.append((cmd, r.rstrip("\r\n")))
        return r

    def query_ascii_values(self, cmd, converter=None):
        return self._real.query_ascii_values(cmd, converter)

    def write(self, cmd):
        self.dialogues.append((cmd, ""))
        return self._real.write(cmd)

    def read_raw(self):
        return self._real.read_raw()

    def close(self):
        return self._real.close()

    @property
    def timeout(self):
        return self._real.timeout

    @timeout.setter
    def timeout(self, value):
        self._real.timeout = value

    @property
    def read_termination(self):
        return self._real.read_termination

    @read_termination.setter
    def read_termination(self, value):
        self._real.read_termination = value

    @property
    def write_termination(self):
        return self._real.write_termination

    @write_termination.setter
    def write_termination(self, value):
        self._real.write_termination = value


def _coerce(raw: str):
    """Coerce a string from ``--set name=value`` to int / float / bool / str."""
    low = raw.lower()
    if low in ("true", "false"):
        return low == "true"
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def _walk_getters(inst, skip):
    """Read every readable property defined on ``inst``'s own class.

    Inherited properties (``Common.config_file``, ``Common.auto_reconnect``,
    etc.) are filtered out because they don't talk to the instrument.
    """
    cls = type(inst)
    for name, attr in vars(cls).items():
        if name.startswith("_") or name in skip:
            continue
        if not isinstance(attr, property) or attr.fget is None:
            continue
        try:
            getattr(inst, name)
            print(f"  captured getter: {name}", file=sys.stderr)
        except Exception as ex:
            print(f"  skipped {name}: {ex}", file=sys.stderr)


def _apply_setters(inst, sets):
    for spec in sets:
        name, _, raw = spec.partition("=")
        if not name or not raw:
            print(f"  malformed --set value: {spec!r}", file=sys.stderr)
            continue
        try:
            setattr(inst, name, _coerce(raw))
            print(f"  captured setter: {name}={raw}", file=sys.stderr)
        except Exception as ex:
            print(f"  failed to set {name}: {ex}", file=sys.stderr)


def _emit_yaml(class_name, address, dialogues):
    """Emit the pyvisa-sim YAML to stdout-style lines."""
    seen = set()
    unique = []
    for q, r in dialogues:
        key = (q, r)
        if key in seen:
            continue
        seen.add(key)
        unique.append((q, r))

    device = class_name.lower()
    lines = [
        'spec: "1.1"',
        "devices:",
        f"  {device}:",
        "    eom:",
        "      TCPIP INSTR:",
        '        q: "\\r\\n"',
        '        r: "\\n"',
        "    error: ERROR",
        "    dialogues:",
    ]
    for q, r in unique:
        # YAML double-quoted strings handle most escapes; escape backslashes
        # and quotes so binary-ish responses survive.
        q_esc = q.replace("\\", "\\\\").replace('"', '\\"')
        if r:
            r_esc = r.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'      - q: "{q_esc}"')
            lines.append(f'        r: "{r_esc}"')
        else:
            lines.append(f'      - q: "{q_esc}"')
    lines.append("resources:")
    lines.append(f"  {address}:")
    lines.append(f"    device: {device}")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "class_name", help="Class name as exposed under bench.all (e.g. N5182B)"
    )
    p.add_argument(
        "address", help="VISA address of the (real or CE-emulated) instrument"
    )
    p.add_argument("--backend", default=None, help="Override pyvisa backend (e.g. @py)")
    p.add_argument(
        "--set",
        dest="sets",
        action="append",
        default=[],
        help="Property setter to exercise, repeatable (e.g. --set frequency=2.4e9)",
    )
    p.add_argument(
        "--skip",
        dest="skip",
        action="append",
        default=["reset"],
        help="Property name to skip during getter walk (default: reset)",
    )
    p.add_argument("--out", default=None, help="Output YAML path (default: stdout)")
    args = p.parse_args(argv)

    cls = getattr(bench_all, args.class_name, None)
    if cls is None:
        print(
            f"Unknown class {args.class_name!r}. Make sure it is exported from bench.all.",
            file=sys.stderr,
        )
        return 2

    inst = cls(address=args.address, backend=args.backend)
    inst.connect()
    inst._instr = Recorder(inst._instr)

    print(f"Walking getters on {args.class_name}...", file=sys.stderr)
    _walk_getters(inst, set(args.skip))

    if args.sets:
        print(f"Exercising {len(args.sets)} setter(s)...", file=sys.stderr)
        _apply_setters(inst, args.sets)

    yaml_text = _emit_yaml(args.class_name, args.address, inst._instr.dialogues)
    if args.out:
        with open(args.out, "w") as f:
            f.write(yaml_text)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(yaml_text)

    inst.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
