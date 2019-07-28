from contextlib import contextmanager
from json import dumps as _json_dumps, loads as _json_loads
from sys import exit as _sys_exit
from pathlib import Path as _pathlib_Path
from typing import Optional, Sequence

import click
from click import UsageError

from .core import scroll, resolve, set_background, _IS_NATIVE_ENVIRONMENT

_CONFIG_PATH = _pathlib_Path('~/.config/bgi').expanduser()

if not _CONFIG_PATH.exists():
    _CONFIG_PATH.mkdir()

_DEFAULT_ALIAS_PATH = _CONFIG_PATH / 'alias.json'



@contextmanager
def fetch_cache(
    *, write_back: bool = False, dry_run: bool = False, fp: str = _DEFAULT_ALIAS_PATH
):
    if not dry_run:
        path = _pathlib_Path(fp)

        if not path.exists():
            with open(str(path), 'w') as inf:
                inf.write(_json_dumps({}))

        mode = 'r+' if write_back else 'r'

        with open(fp, mode) as inf:
            data = _json_loads(inf.read())

            yield data

            if write_back:
                inf.seek(0)
                _json_dumps(data, inf)
    else:
        yield {}


@click.command()
@click.option('-a', '--add-alias', is_flag=True)
@click.option('-r', '--remove-alias', is_flag=True)
@click.option('-l', '--list-alias', is_flag=True)
@click.option('-L', '--local', default=None, type=str)
@click.option('--speed', default=1, type=float)
@click.argument('target', nargs=-1)
def main(
    add_alias: bool,
    remove_alias: bool,
    list_alias: bool,
    local: Optional[str],
    speed: Optional[float],
    target: Sequence[str],
):
    if target:
        action, *_ = target
    else:
        raise UsageError('Please supply a target.')

    if (
        action in ('loop', 'scroll', 'random')
        and not _IS_NATIVE_ENVIRONMENT
        and local is None
    ):
        _sys_exit(
            'You must specify a directory to source images from with the `-L`/`--local` argument'
        )

    alias_action = any((list_alias, add_alias, remove_alias))
    dry_run = (not alias_action) and action in ('loop', 'scroll', 'random')

    with fetch_cache(write_back=list_alias, dry_run=dry_run) as data:
        if alias_action:
            if list_alias:
                print(
                    '\n'.join(f'{name!r} => {value!r}' for name, value in data.items())
                )

            elif add_alias:
                src, dst = target
                data[src] = dst

            else:
                for name in target:
                    del data[name]

        elif action in ('loop', 'scroll'):
            scroll(
                iterations=(0 if action == 'loop' else iterations),
                delay=speed,
                directory=local,
                images=((resolve(part, data) for part in target) if target else None),
            )

        else:
            image = (
                resolve(target[-1], data=data) if action != 'random' else fetch_image()
            )

            set_background(image)


if __name__ == '__main__':
    main()
