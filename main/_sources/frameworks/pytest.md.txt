# pytest

pybench can be integrated with pytest by either directly using instrument classes or by leveraging the `pytest` fixtures provided by pybench. The fixtures are designed to help manage the lifecycle of the instrument and the data acquisition process. This also includes requiring instruments for tests, or making them interchangeable based on what a user has physical access to.

## CLI options

The following CLI options are available for use with pytest:

- `--confifile`: Path to the configuration file to use for the test run. If not provided, the default configuration file will be used. This is the configuration that defines which instruments are available and their addresses.

## Available fixtures

The following fixtures are available for use in your tests:

- `instrument_addresses`: A fixture that returns a list of all available instruments of those specified in the configuration file.
- `instrument_address_session`: A fixture that returns a session-scoped instrument address. This is useful for tests that require an instrument to be available for the duration of all tests.