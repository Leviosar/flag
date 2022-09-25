import click
from pathlib import Path
from flagg.handlers import cli_handler

@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.option("--output", type=click.Path(path_type=Path))
@click.option("--verbose/--no-verbose", default=False)
@click.option("--syntatic/--no-syntatic", default=False)
def cli(input, source, output, verbose, syntatic):
    return cli_handler(input, source, output, verbose, syntatic)

if __name__ == "__main__":
    cli()
