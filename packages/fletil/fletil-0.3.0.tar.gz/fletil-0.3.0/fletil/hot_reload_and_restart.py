"""Hot reload and restart functionality."""


import atexit
import gc
import time
import sys
from collections import defaultdict
from functools import partial
from importlib import util
from pathlib import Path
from types import ModuleType
from typing import Literal

import flet
import flet.colors
from loguru import logger
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from fletil.utils import (
    STATE_ATTRS_REGISTRY,
    add_dev,
    checkif_import_friendly,
    inplace_recurse_controls,
)


class Handler(PatternMatchingEventHandler):
    """Filesystem events handler."""

    def __init__(self, module, target_name):
        self._module = module
        self._target_name = target_name
        self._page = None
        self._extra_data = {}
        self._last_time = time.time()
        super().__init__(patterns=["*.py"], ignore_directories=True)
        return

    def on_any_event(self, event, reload_=True):
        """Perform a `reload` or `restart` if the event is relevant."""
        if event.event_type in [
                "created",
                "modified",
                "deleted",
        ]:
            now = time.time()

            if (now - self._last_time) < 5:
                return
            self._last_time = now
            logger.info(f"{event.event_type.title()}: {event.src_path}")
            path = event.src_path
            src = Path(path).read_text()
            page = self._page
            dev_buttons = getattr(
                page,
                "__fletil__dev_buttons",
                type(
                    "FakeRow",
                    (),
                    {"set_code_status": lambda *a, **k: None},
                )(),
            )
            set_code_status = partial(dev_buttons.set_code_status, page)

            try:
                compile(src, "", "exec")

            except SyntaxError:
                msg = "Aborted reload due to Syntax error..."
                logger.error(msg)
                set_code_status(flet.colors.RED, msg)
                return

            if not checkif_import_friendly(src, raise_=False):
                msg = "Aborted reload as not import friendly..."
                logger.error(msg)
                set_code_status(flet.colors.ORANGE, msg)
                return
            o_module = None

            for attr in list(sys.modules.values()):
                maybe_path = getattr(attr, "__file__", "")

                if Path(maybe_path).resolve() == Path(path).resolve():
                    o_module = attr
                    break

            else:
                msg = f'Something went wrong seeking module at {path}'
                logger.error(msg)
                set_code_status(
                    flet.colors.YELLOW_100, msg)
                return
            module_name = o_module.__name__
            spec = util.spec_from_file_location(
                module_name, path)
            n_module = util.module_from_spec(spec)
            spec.loader.exec_module(n_module)
            o_refs = gc.get_referrers(o_module)

            for ref in o_refs:
                if isinstance(ref, dict):
                    for key, val in ref.items():
                        if val is o_module and key != "o_module":
                            ref[key] = n_module

                else:
                    exc = TypeError(f"Got a non-dict: {ref}")
                    logger.warning(repr(exc))
            target = getattr(n_module, self._target_name)
            assert callable(target), f'"{self._target_name}" is not a function'
            hor, ver = self._extra_data.get("dev_buttons", [None] * 2)

            if hor and ver:
                target = add_dev(hor, ver, target)
            controls = page.controls
            state = defaultdict(lambda: {})

            try:
                if reload_:
                    inplace_recurse_controls(
                        partial(update_state, state, "save"), page)
                page.controls.clear()
                page.update()
                target(page)

                if reload_:
                    inplace_recurse_controls(
                        partial(update_state, state, "load"), page)
                    page.update()

            except Exception as exc:
                page.controls = controls
                page.update()
                logger.exception(
                    f"{'Reload' if reload_ else 'Restart'} failed")

                if reload_:
                    return self.on_any_event(event, reload_=False)
                set_code_status(
                    flet.colors.RED, repr(exc))

            else:
                msg = f"Source {'reloaded' if reload_ else 'restarted'}"
                logger.info(msg)
                set_code_status(flet.colors.GREEN, msg)
        return

    def set_page(self, page: flet.Page, **extra_data):
        """Save the default page and any extra data.

        This method is called by a decorator which wraps the target
        function.
        """
        if not self._page:
            self._page = page
            self._extra_data = extra_data
        return


def update_state(
        state: dict,
        mode: Literal["load", "save"],
        control: flet.Control,
) -> None:
    """Save/load relevant state for a given control."""
    data = control.data
    c_name = type(control).__name__
    cid = None
    state_attrs = []

    if isinstance(data, str) and data.startswith("_cid:"):
        cid = data.partition(":")[2]

    elif isinstance(data, dict) and "_cid" in data:
        cid = str(data["_cid"])
        state_attrs = data.get("_state_attrs", [])
    state_attrs += STATE_ATTRS_REGISTRY.get(c_name, [])

    if cid:
        if mode == "save" and cid in state:
            raise KeyError(f'Duplicate cid "{cid}"')

        for name in state_attrs:
            if mode == "save":
                state[cid][name] = getattr(control, name)

            elif mode == "load":
                setattr(control, name, state[cid][name])
    return


def cleanup(observer):
    """Gracefully terminate the watcher upon exit."""
    logger.info("Terminating watcher...")
    observer.stop()
    observer.join()
    return


def get_page(handler, target, **extra_data):
    """Collect the original page with which the app's target is called."""

    def _get(page):
        handler.set_page(page, **extra_data)
        return target(page)
    return _get


def watch(module, target_name):
    """Create a watcher for the project."""
    handler = Handler(module, target_name)
    observer = Observer()
    path = Path(module.__file__).parent
    observer.schedule(handler, str(path), recursive=True)
    atexit.register(cleanup, observer)
    observer.start()
    logger.info(f"Watching for changes in {path}")
    return partial(get_page, handler)
