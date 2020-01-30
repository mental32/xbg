__version__ = "0.2.0"
__author__ = "mental"
__license__ = "MIT"

from random import choice
from subprocess import check_call
from pathlib import Path
from time import sleep

import click
from click import BadParameter, Choice


_ACTION_CHOICES = Choice(["loop", "scroll", "random", "set"])


@click.command()
@click.argument("target", type=Path)
@click.option("--action", type=_ACTION_CHOICES, default="set")
@click.option("--delay", type=float, default=1.0)
def main(*, target: Path, action: str, delay: float):
    if not target.exists():
        raise BadParameter(
            "`target` argument must exist and point to a image or directory of images."
        )

    files = [
        str(part)
        for part in (target.iterdir() if target.is_dir() else [target])
        if not part.is_dir()
    ]

    multiple = len(files) > 1

    if multiple and action in ("random", "set"):
        files = [choice(files)]
        multiple = False

    while True:
        for image in files:
            check_call(f"feh --bg-fill {image!s}", shell=True)

            if multiple:
                sleep(delay)

        if action != "loop":
            break


if __name__ == "__main__":
    main()  # pylint: disable=missing-kwoa
