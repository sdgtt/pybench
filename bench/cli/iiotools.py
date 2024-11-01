import os
import subprocess
import time

import click
import requests

from bench.keysight.dwta.data_capture import capture_iq_datafile

try:
    import iio
except ImportError:
    click.echo("IIO not found, please install pylibiio")
    exit(1)


@click.group()
@click.option("--uri", "-u", help="URI of target device/board")
@click.pass_context
def cli(ctx, uri):
    """Command line interface for pybench IIO based boards"""
    ctx.obj = {}
    ctx.obj["uri"] = uri


@cli.command()
@click.option(
    "--frequency", "-f", help="Set the frequency of the DDS in Hz", required=True
)
@click.option(
    "--amplitude", "-a", help="Set the amplitude of the DDS in 0->1", required=True
)
@click.option("--device", "-d", help="IIO device driver name to use")
@click.option("--channel", "-c", help="Set the channel of the DDS", required=True)
@click.option("--complex", "-x", is_flag=True, help="Use complex mode")
@click.pass_context
def set_dds(ctx, frequency, amplitude, device, channel, complex):
    """Configure DDS"""
    iioctx = iio.Context(ctx.obj["uri"])
    if not iioctx:
        click.echo("No context")
        return
    dev = iioctx.find_device(device)
    if not dev:
        click.echo(f"Device {device} not found")
        return
    dds_channels = [ch.id for ch in dev.channels if "altvoltage" in ch.id]
    # Set all the DDS scales to 0
    dds_channels.sort(key=lambda x: int(x.replace("altvoltage", "")))
    for ch in dds_channels:
        chan = dev.find_channel(ch, True)
        if not chan:
            click.echo(f"Channel {ch} not found")
            return
        chan.attrs["scale"].value = "0"
    # Set the desired DDS scale
    if complex:
        # Channels are groups of 4
        ch = int(channel) * 4
        channels = [ch, ch + 1]
    else:
        ch = int(channel) * 2
        channels = [ch, ch + 1]

    for i, ch in enumerate(channels):
        chan = dev.find_channel(f"altvoltage{ch}", True)
        if not chan:
            click.echo(f"Channel {ch} not found")
            return
        chan.attrs["frequency"].value = frequency
        chan.attrs["scale"].value = amplitude
        if complex:
            # i is odd
            if i % 2:
                chan.attrs["phase"].value = "90000"
            else:
                chan.attrs["phase"].value = "0"

    click.echo(f"Set DDS of channel {channel} to {frequency}Hz and {amplitude} scale")


@cli.command()
@click.option("--filename", "-f", help="Name of file to write data to", required=True)
@click.option("--device", "-d", help="Name of device to configure", required=True)
@click.option(
    "--channel",
    "-c",
    help="Channel index to capture data from. Starts from 0",
    required=True,
)
@click.option("--samples", "-s", help="Number of samples to capture", required=True)
@click.argument(
    "props", nargs=-1, required=False,
)
@click.pass_context
def capture_data(ctx, filename, device, channel, samples, props):
    """Capture IQ data to a file in DWTA format

    PROPS is a list of property=value pairs to set device properties. These are
    the properties available in the pyadi-iio class interface for the device.

    Example usage with ADALM-PLUTO:

        pybenchiio -u ip:analog.local capture_data -f data.csv -d Pluto -c 0 -s 1024 sample_rate=1000000
    """
    # Checks
    samples = int(samples)
    channel = int(channel)

    # Parse properties
    if props:
        oprops = {}
        for prop in props:
            if "=" not in prop:
                raise ValueError(
                    f"Invalid property: {prop}. Must be in the form key=value\n",
                    "or key=value,index for array properties",
                )
            k, v = prop.split("=")
            if "," in v:
                v = v.split(",")
                assert len(v) == 2, "Invalid array property"
                v = v[0]
                assert v.isdigit(), "Invalid array index property"
                index = int(v[1])
            else:
                index = -1
            if v.isdigit():
                v = int(v)
            oprops[k] = {"value": v, "index": index}
        props = oprops

    capture_iq_datafile(
        filename, device, channel, samples, ctx.obj["uri"], **dict(props)
    )


@cli.command()
@click.option("--filename", "-f", help="Name of file to write data to", required=True)
@click.option("--device", "-d", help="Name of device to configure", required=True)
@click.option("--channel", "-c", help="Channel to capture data from", required=True)
@click.option(
    "--server-ip",
    "-s",
    help="IP address of the server",
    required=False,
    default="localhost",
)
@click.option(
    "--server-port", "-p", help="Port of the server", required=False, default=12345
)
@click.argument("props", nargs=-1)
@click.pass_context
def transmit_data(ctx, filename, device, channel, server_ip, server_port, props):
    """Transmit IQ data file to device through backend server

    File must be in DWTA format, where the first two lines are sample rate and
    center frequency, and the rest of the lines are IQ data in the format
    I, Q per line.

    Example usage with ADALM-PLUTO:

        pybenchiio -u ip:analog.local transmit_data -f data.csv -d Pluto -c 0 sample_rate=1000000
    """

    # Checks
    channel = int(channel)

    # Parse properties
    # if props:
    #     oprops = {}
    #     for prop in props:
    #         if "=" not in prop:
    #             raise ValueError(
    #                 f"Invalid property: {prop}. Must be in the form key=value"
    #             )
    #         k, v = prop.split("=")
    #         if v.isdigit():
    #             v = int(v)
    #         oprops[k] = v
    #     props = oprops

    # transmit_iq_datafile(
    #     filename, device, channel, ctx.obj["uri"], **dict(props)
    # )

    import os

    import requests

    # Send post request to localhost
    url = f"http://{server_ip}:{server_port}/writebuffer"
    json_data = {
        "uri": ctx.obj["uri"],
        "device": device,
        "channel": channel,
        "data_filename": filename,
        "do_scaling": False,
        "cycle": True,
        "data_complex": True,
        "properties": props,
    }
    r = requests.post(url, json=json_data)
    assert r.status_code == 200, f"Failed to send data: {r.json()}"


@cli.command()
@click.option(
    "--server-ip",
    "-s",
    help="IP address of the server",
    required=False,
    default="localhost",
)
@click.option(
    "--server-port", "-p", help="Port of the server", required=False, default=12345
)
def transmit_data_clear(server_ip, server_port):
    """Clear the transmit buffer on the server"""

    url = f"http://{server_ip}:{server_port}/clearbuffer"
    r = requests.post(url)
    assert r.status_code == 200, f"Failed to clear buffer: {r.json()}"


@cli.command()
@click.option(
    "--host",
    "-h",
    help="Host to start the server on",
    required=False,
    default="localhost",
)
@click.option(
    "--port", "-p", help="Port to start the server on", required=False, default=12345
)
def start_server(host, port):

    # Start the server as a subprocess
    import os
    import subprocess

    loc = os.path.dirname(os.path.realpath(__file__))
    web_app = os.path.join(loc, "..", "web", "app.py")
    web_app = os.path.abspath(web_app)

    # Get location of python executable
    python = "python"
    if "CONDA_PREFIX" in os.environ:
        python = os.path.join(os.environ["CONDA_PREFIX"], "bin", "python")
    elif "VIRTUAL_ENV" in os.environ:
        python = os.path.join(os.environ["VIRTUAL_ENV"], "bin", "python")
    elif "PYTHON" in os.environ:
        python = os.environ["PYTHON"]

    command = [
        python,
        "-m",
        "fastapi",
        "run",
        web_app,
        "--host",
        str(host),
        "--port",
        str(port),
    ]
    # Start process and verify running after 5 seconds
    p = subprocess.Popen(command)
    time.sleep(5)
    assert p.poll() is None, "Failed to start server"
    print(f"Server started on {host}:{port} with PID {p.pid}")


# Stop server
@cli.command()
@click.option(
    "--server-port", "-p", help="Port of the server", required=False, default=12345
)
def stop_server(server_port):
    """Stop the server"""
    # Find the process using the port and kill it
    if os.name == "nt":
        # Query for the process ID
        pid = subprocess.run(
            f"netstat -aon | findstr {server_port}", shell=True, stdout=subprocess.PIPE
        )
        if pid.returncode != 0:
            print("Server not running")
            return
        pid = pid.stdout.decode().split(" ")[-1]
        # Kill the process
        subprocess.run(f"taskkill /F /PID {pid}", shell=True)
    else:
        # Query for the process ID
        pid = subprocess.run(
            f"lsof -t -i:{server_port}", shell=True, stdout=subprocess.PIPE
        )
        if pid.returncode != 0:
            print("Server not running")
            return
        pid = pid.stdout.decode().strip()
        print(f"Server found on port {server_port} with PID {pid}")
        # Kill the process
        subprocess.run(f"kill -9 {pid}", shell=True)

    print(f"Server on port {server_port} stopped")
