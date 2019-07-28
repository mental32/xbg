from asyncio import Event as _asyncio_Event
from glob import glob as _glob_glob
from itertools import count as _itertools_count
from json import dumps as _json_dumps
from os import fdopen as _os_fdopen
from pathlib import Path as _pathlib_Path
from subprocess import check_output as _subprocess_check_output
from tempfile import mkstemp as _tempfile_mkstemp
from time import sleep as _time_sleep
from typing import Sequence, Optional, Union

__all__ = ('resolve', 'set_background', 'scroll')

_DEFAULT_DEST = '/usr/share/background'

try:
    _SYS_DAEMON_VERSION = _subprocess_check_output('dae --version').decode().strip()
except Exception:
    _IS_NATIVE_ENVIRONMENT = False
else:
    _IS_NATIVE_ENVIRONMENT = True


async def _fetch_image_routine(daemon_module, daemon, kwargs):
    """The internal routine invoked by the daemon."""
    if not _IS_NATIVE_ENVIRONMENT:
        raise RuntimeError('A native environment is required to call this helper.')

    client = daemon.discord_user_presence

    user_id = 475830155667963924
    user = client.get_user(user_id)

    if user is None:
        raise daemon_module.errors.FooBarException

    fetch, name = kwargs['fetch'], kwargs['name']

    event = _asyncio_Event(loop=client.loop)
    event.clear()

    async def listener(flag):
        flag.set()
        message = await client.wait_for(
            'message',
            check=(
                lambda m: m.guild is None and m.author.id == user_id and m.attachments
            ),
        )

        image, *_ = message.attachments

        fd, name = _tempfile_mkstemp()

        with _os_fdopen(fd, 'w') as inf:
            inf.write(image.read(use_cached=True))

        # The other end is a `check_output`
        # call in `fetch_image` that operates
        # on the stdout of this routine.
        print(name)

    listener_task = client.loop.create_task(listener(event))

    await event.wait()
    await user.send(f'?fs {fetch} {name}')
    await asyncio.gather(listener_task)


def fetch_image(name: Optional[str] = None) -> _pathlib_Path:
    """Ask the system daemon to fetch an image.

    Parameters
    ----------
    name : Optional[str]
        The name of the image to fetch,
        when not provided a random image
        is selected.
    """
    if not _IS_NATIVE_ENVIRONMENT:
        raise RuntimeError('A native environment is required to call this helper.')

    data = {'fetch': 'rfetch' if name is None else 'fetch', 'name': name or ''}

    command = f'dae -m "{__name__}:_fetch_image_routine;{_json_dumps(data)}"'
    return _pathlib_Path(_subprocess_check_output(command).decode().strip())


def set_background(image: str):
    """Set the background image.

    Parameters
    ----------
    image : str
        The path to the image to use.
    """
    raise NotImplementedError


def scroll(
    iterations: Optional[int] = 1,
    delay: Optional[int] = 1,
    *,
    directory: Optional[str],
    images: Optional[Sequence[Union[_pathlib_Path, str]]] = None,
) -> None:
    """Iterate through background images.

    Parameters
    ----------
    iterations : Optional[int]
        The amount of iterations
        to perform over the entire
        set of images. By default
        the amount is set to 1. When
        set to a value less than 1 it
        will iterate infinitely.
    delay : Optional[int]
        The amount of time, in
        seconds to pause before
        moving onto the next image.
        by default the delay is set
        to 1.
    directory : Optional[str]
        The directory to source
        the images from, when not
        provided the system daemon is
        consulted.
    images : Optional[Sequence[Union[Path, str]]]
        A sequence of pathlib.Path objects or strings
        that point to images to target, this is how you'd
        filter for a subset of images.
    """
    assert isinstance(delay, int)
    assert isinstance(iterations, int)
    assert directory is None or isinstance(directory, str)
    assert images is None or hasattr(images, '__iter__') or hasattr(images, '__next__')

    cycle = _itertools_count() if iterations < 1 else range(iterations)

    for iteration in cycle:
        if directory is not None:
            images = (
                file
                for file in _glob_glob(f'{directory}/**/*')
                if file.endswith(('.jpg', '.png'))
            )
        else:
            images = (file for file in oof)  # XXX

        for image in images:
            set_background(image)
            _time_sleep(delay)


def resolve(name: str, data: dict) -> _pathlib_Path:
    """Resolve an alias into a name then fetch_image.

    Parameters
    ----------
    name : str
        The name to resolve.
    data : dict
        The mapping of alias to names.
    """

    if _IS_NATIVE_ENVIRONMENT:
        func = fetch_image
    else:
        func = _pathlib_Path

    return func(data[name[1:]] if name[0] == '@' else name)
