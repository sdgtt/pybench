import click

import iio

@click.group()
@click.option("--uri", "-u", help="URI of target device/board")
@click.option("--device", "-d", help="Device driver to use")
@click.option("--complex", "-x", is_flag=True, help="Use complex mode")
@click.pass_context
def cli(ctx, uri, device, complex):
    """Command line interface for pybench IIO based boards"""
    ctx.obj = {}
    ctx.obj["uri"] = uri
    ctx.obj["device"] = device
    ctx.obj["complex"] = complex


@cli.command()
@click.option("--attribute", "-a", help="Attribute to access", required=True)
@click.pass_context
def get(ctx, attribute):
    """Get an attribute from a device"""
    click.echo(f"Get {attribute} from {ctx.obj['uri']}")

@cli.command()
@click.option("--frequency", "-f", help="Set the frequency of the DDS in Hz", required=True)
@click.option("--amplitude", "-a", help="Set the amplitude of the DDS in 0->1", required=True)
@click.option("--channel", "-c", help="Set the channel of the DDS", required=True)
@click.pass_context
def set_dds(ctx, frequency, amplitude, channel):
    """Configure DDS"""
    iioctx = iio.Context(ctx.obj["uri"])
    if not iioctx:
        click.echo("No context")
        return
    dev = iioctx.find_device(ctx.obj["device"])
    if not dev:
        click.echo(f"Device {ctx.obj['device']} not found")
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
    if ctx.obj["complex"]:
        # Channels are groups of 4
        ch = int(channel) * 4
        channels = [ch, ch + 1]
    else:
        ch = int(channel)*2
        channels = [ch, ch + 1]

    for i, ch in enumerate(channels):
        chan = dev.find_channel(f"altvoltage{ch}", True)
        if not chan:
            click.echo(f"Channel {ch} not found")
            return
        chan.attrs["frequency"].value = frequency
        chan.attrs["scale"].value = amplitude
        if ctx.obj["complex"]:
            # i is odd
            if i % 2:
                chan.attrs["phase"].value = "90000"
            else:
                chan.attrs["phase"].value = "0"

    click.echo(f"Set DDS of channel {channel} to {frequency}Hz and {amplitude} scale")
    


