# Installation

The module is compatible with Python 3.6 and above. It is recommended to use a virtual environment to install the module. To install the module, run the following command:

```bash
python -m venv venv
(Windows) venv\Scripts\activate
(Linux) source venv/bin/activate
pip install pybench
```

The majority of the dependencies are installed via `pip` when installing the module or by using the `requirements.txt` file when using the source repo. However, there are some dependencies that need to be installed manually for certain instruments to work or improve their functionality.

## Keysight

Its recommended you install the IO Libraries and Drivers to communicate with instruments.
- [IO Libraries Suite Downloads](https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html)
