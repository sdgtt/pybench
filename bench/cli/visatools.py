import click
import pyvisa


@click.group()
@click.pass_context
def cli(ctx, uri):
    """Command line interface for pybench VISA based instruments"""
    ctx.obj = {}
    ctx.obj["uri"] = uri

@cli.command()
@click.pass_context
def list(ctx, attribute):
    """List available devices"""
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    for resource in resources:
        click.echo(resource)
