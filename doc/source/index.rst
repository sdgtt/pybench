.. pybench documentation master file, created by
   sphinx-quickstart on Wed May 15 06:07:15 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pybench: Lab Bench Instrument Controls in Python
================================================

pybench is a Python package for controlling lab bench instruments. It is designed to be easy to use and to provide a consistent interface to a wide variety of instruments. pybench primarily uses the VISA standard for instrument communication, but supports other communication methods as well.

The module is designed to also support testing frameworks, such as pytest, and to support modern CI driven development and testing.

.. toctree::
   :maxdepth: 1
   :caption: User Guide

   install.md
   example_usage
   instruments/index
   cli


.. toctree::
   :maxdepth: 1
   :caption: Frameworks

   frameworks/pytest


.. toctree::
   :maxdepth: 1
   :caption: Special Functionality

   config_file

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Disclaimer
==========

This package is not endorsed by or affiliated with any of the instrument manufacturers. It is a community driven project and is not officially supported by any of the instrument manufacturers.
