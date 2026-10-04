import click

from execution_engine import run_program


@click.group()
def cli():
    """PyChronicle - Time-Travel Debugger for Python."""
    pass


@cli.command()
@click.argument("filename")
def run(filename):
    """Run a Python file with PyChronicle."""
    run_program(filename)


if __name__ == "__main__":
    cli()