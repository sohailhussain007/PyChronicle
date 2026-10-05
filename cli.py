import click

from execution_engine import run_program
from storage.state_storage import SQLiteStateStorage


DATABASE_FILE = "pychronicle.db"


@click.group()
def cli():
    """PyChronicle - Time-Travel Debugger for Python."""
    pass


@cli.command()
@click.argument("filename")
@click.option("--watch", "watch_variable", default=None)
def run(filename, watch_variable):
    """Run a Python file with PyChronicle."""

    run_program(filename)

    if watch_variable:
        click.echo(f"\nWatching variable: {watch_variable}")

        storage = SQLiteStateStorage(DATABASE_FILE)
        states = storage.get_states(watch_variable)
        storage.close()

        if states:
            for timestamp, line_number, variable_name, value in states:
                click.echo(
                    f"Line {line_number} -> "
                    f"{variable_name} = {value}"
                )
        else:
            click.echo(
                f"Variable '{watch_variable}' was not found."
            )


if __name__ == "__main__":
    cli()