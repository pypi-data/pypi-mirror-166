from pathlib import Path
from typing import List, Optional

import typer
from atomkraft.config.atomkraft_config import AtomkraftConfig

from .model import MODEL_CONFIG_KEY, test_model
from .trace import test_trace

app = typer.Typer(rich_markup_mode="rich", add_completion=False)


def FileOption(help, default):
    return typer.Option(
        None,
        exists=True,
        file_okay=True,
        dir_okay=False,
        show_default=False,
        help=f"{help} [grey30][default: set via [bold cyan]atomkraft {default}[/bold cyan]][/grey30]",
    )


def RequiredFileOption(help, default):
    return typer.Option(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        show_default=False,
        help=f"{help} [grey30][default: set via [bold cyan]atomkraft {default}[/bold cyan]][/grey30]",
    )


@app.command()
def trace(
    # currently, require the trace to be present.
    # later, there will be an option to pick up the last one from the model
    trace: Path = RequiredFileOption("trace to execute", "model"),
    reactor: Optional[Path] = FileOption("reactor to interpret the trace", "reactor"),
    keypath: str = typer.Option(
        "action",
        show_default=True,
        help="Path to key used as step name, extracted from ITF states",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Output logging on console"
    ),
):
    """
    Test blockchain by running one trace
    """

    exit_code = test_trace(trace, reactor, keypath, verbose)

    raise typer.Exit(exit_code)


@app.command()
def model(
    model: Optional[Path] = FileOption("model used to generate traces", "model"),
    config: Optional[Path] = FileOption("model configuration", "model"),
    test: List[str] = typer.Option(
        None,
        show_default=False,
        help="model operator(s) describing test traces. multiple can be given either comma-separated, or via separate --test options",
    ),
    reactor: Optional[Path] = FileOption("reactor to interpret the traces", "reactor"),
    keypath: str = typer.Option(
        "action",
        show_default=True,
        help="Path to key used as step name, extracted from ITF states",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Output logging on console"
    ),
):
    """
    Test blockchain by running multiple traces generated from a model
    """
    tests = [t.strip() for ts in test for t in ts.split(",")]

    exit_code = test_model(model, tests, reactor, keypath, verbose)

    if model:
        with AtomkraftConfig() as c:
            c[MODEL_CONFIG_KEY] = str(model)

    raise typer.Exit(exit_code)
