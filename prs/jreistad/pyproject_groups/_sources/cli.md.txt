# Command Line Interface Tools

The following command line tools are available in the when the optional `cli` dependency is installed.

```bash
pip install pybench[cli]
```

There are two command line tools available:
- [`pybenchiio`](#pybenchiiocli) - A command line tool for interfacing with libiio devices.
- [`pybench`](#pybenchcli) - A command line tool for querying VISA based instruments.

## Keysight DMX

One of the main use cases for the CLI pybench tools is to support the Keysight Device Manager eXpert (DMX) software. The DMX software is a tool for managing and configuring Keysight instruments. The `pybench` CLI tool provides a way for the DMX software to communicate with pybench instruments and devices.

Since the DMX software uses single commands to perform data capture and data generation this required additional infrastructure specifically for IIO based systems. IIO based systems do not maintain persistent buffer when leveraging custom data vectors through DMA channels. Essentially, when the contexts are closed the buffers clear and the IIO based system will revert back to the DDS data generation state. To solve this problem a backend server was implemented to maintain these buffers that is controlled by the `pybenchiio` CLI tool. See the [pybenchiio](#pybenchiiocli) section for more information.


## Reference APIs

(pybenchiiocli)=
```{eval-rst}
.. click:: bench.cli.iiotools:cli
   :prog: pybenchiio
   :nested: full


```

---

(pybenchcli)=
```{eval-rst}
.. click:: bench.cli.visatools:cli
   :prog: pybench
   :nested: full


```
