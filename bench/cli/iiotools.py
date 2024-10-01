import click
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
@click.option("--device", "-d", help="Device driver to use")
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
@click.option("--channel", "-c", help="Channel to capture data from", required=True)
@click.option("--samples", "-s", help="Number of samples to capture", required=True)
@click.argument("props", nargs=-1)
@click.pass_context
def capture_Data(ctx, filename, device, channel, samples, props):

    # Checks
    samples = int(samples)

    # Parse properties
    if props:
        oprops = {}
        for prop in props:
            if "=" not in prop:
                raise ValueError(
                    f"Invalid property: {prop}. Must be in the form key=value"
                )
            k, v = prop.split("=")
            if v.isdigit():
                v = int(v)
            oprops[k] = v
        props = oprops

    capture_iq_datafile(
        filename, device, channel, samples, ctx.obj["uri"], **dict(props)
    )
