import click

from execution_engine import run_program
from state_reconstruction import get_timeline_for_ui


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

        timeline = get_timeline_for_ui("pychronicle.db")

        found = False

        for item in timeline:
            if watch_variable in item["state"]:
                value = item["state"][watch_variable]

                click.echo(
                    f"Line {item['line_number']} -> "
                    f"{watch_variable} = {value}"
                )

                found = True

        if not found:
            click.echo(
                f"Variable '{watch_variable}' was not found."
            )


if __name__ == "__main__":
    cli()