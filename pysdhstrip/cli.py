#!/usr/bin/env python3

import logging

try:
    import click
    import cloup
    import coloredlogs
except ModuleNotFoundError:
    raise ImportError(
        "pysdhstrip was installed without the cli extra. "
        'Please reinstall it with: pip install "pysdhstrip[cli]"'
    )

from cloup.constraints import mutually_exclusive

from pysdhstrip import strip


@cloup.command()
@cloup.argument(
    "input_",
    metavar="[INPUT]",
    type=click.Path(exists=True, dir_okay=False, allow_dash=True),
    help="Input file (use - for stdin).",
)
@cloup.option(
    "-o",
    "--output",
    type=click.Path(writable=True, dir_okay=False, allow_dash=True),
    default="-",
    help="Output file (default: stdout; unless -w is used).",
)
@cloup.option(
    "-w",
    "--write",
    is_flag=True,
    help="Overwrite input file.",
)
@cloup.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Suppress warnings.",
)
@cloup.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Show each performed replacement.",
)
@cloup.constraint(mutually_exclusive, ["quiet", "verbose"])
def cli(input_: str, *, output: str, write: bool, quiet: bool, verbose: bool) -> None:
    if quiet:
        level = logging.ERROR
    elif not verbose:
        level = logging.WARNING
    else:
        level = logging.INFO

    coloredlogs.install(
        level=level,
        field_styles={
            "asctime": {"color": 244},
            "levelname": {"color": 248},
            "name": {"color": "blue"},
        },
        fmt="{asctime} [{levelname[0]}] {name}\x1b[0m: {message}",
        style="{",
    )

    with click.open_file(input_) as fd:
        subtitles = fd.read()

    result = strip(subtitles)

    if write:
        output = input_
    with click.open_file(output, "w") as fd:
        fd.write(result)
