# Command Line Interface Tools

The following command line tools are available in the when the optional `cli` dependency is installed. 

```bash
pip install pybench[cli]
```

There are two command line tools available:
- [`pybenchiio`](#pybenchiio) - A command line tool for interfacing with libiio devices.
- [`pybench`](#pybench) - A command line tool for querying VISA based instruments.


(#pybenchiio)=
```{eval-rst}
.. click:: bench.cli.iiotools:cli
   :prog: pybenchiio
   :nested: full


```

---

(#pybench)=
```{eval-rst}
.. click:: bench.cli.visatools:cli
   :prog: pybench
   :nested: full


```