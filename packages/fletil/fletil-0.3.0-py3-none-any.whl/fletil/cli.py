#!/usr/bin/env python3

"""
CLI for fletil (Flet utility).

Type `fletil --help` for usage.
"""


import sys
from importlib import import_module
from pathlib import Path

import fire
import flet

from fletil.hot_reload_and_restart import watch
from fletil.utils import add_dev, checkif_import_friendly


class Commands:
    """A CLI for the Flet framework."""

    def run(
            self,
            app: str,
            host: str = None,
            port: int = 0,
            browser: bool = False,
            assets_dir: str = None,
            web_renderer: flet.WebRenderer = "canvaskit",
            reload: bool = False,
            dev_buttons: str = None,
    ):
        """Run the specified app.

        Args:
          app: Pointer to the app to run, formatted `module.path:main_func`.
          host: Hostname to connect as.
          port: Port to allow connecting on.
          browser: Open the app in a web browser.
          assets_dir: Path to assets directory.
          web_renderer: Render method; options are "canvaskit" and "html".
          reload: Enable hot reload on source file modification.
          dev_buttons: Add dev buttons at the point specified.
            Options are a combination of "top"/"bottom" and
            "left"/"center"/"right" separated by "-", eg. "top-left".
        """
        sys.path.append(".")
        module_path, _, target_name = app.rpartition(":")
        src_path = Path(
            module_path.replace(".", "/")).with_suffix(".py")
        checkif_import_friendly(src_path.read_text())
        module = import_module(module_path)
        target = getattr(module, target_name)
        extra_data = {}

        if not callable(target):
            raise TypeError(f'"{target_name}" is not a function')

        if dev_buttons:
            # TODO: maybe move body to other module
            v, _, h = str(dev_buttons).partition("-")
            h_ok = any([h_pos == h for h_pos in ("left", "center", "right")])
            v_ok = (v == "top") or (v == "bottom")

            if not (v_ok and h_ok):
                msg = f'invalid value "{dev_buttons}" for --dev-buttons'
                raise ValueError(msg)

            else:
                extra_data["dev_buttons"] = (h, v)
                target = add_dev(h, v, target)

        if reload:
            get_page = watch(module, target_name)
            target = get_page(target, **extra_data)
        return flet.app(
            host=host,
            port=port,
            target=target,
            view=flet.FLET_APP if not browser else flet.WEB_BROWSER,
            assets_dir=assets_dir,
            web_renderer=web_renderer,
        )


def run():
    """Run the CLI."""
    return fire.Fire(Commands())


if __name__ == "__main__":
    run()
