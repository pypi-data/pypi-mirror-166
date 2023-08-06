"""Utilities."""


import ast
import sys
from functools import partial
from pathlib import Path

import flet
import flet.colors
from flet.control import Control


STATE_ATTRS_REGISTRY = {
    "TextField": ["value"],
}


def checkif_import_friendly(src, raise_=True):
    last = ast.parse(src).body[-1]

    if isinstance(last, ast.Expr) and isinstance(last.value, ast.Call):
        if raise_:
            raise RuntimeError(
                f"Call `{ast.unparse(last)}` must be under an `if` statement")

        else:
            return False
    return True


def is_control_or_list_of(obj):
    return isinstance(obj, Control) or (
        isinstance(obj, list) and all(
            [isinstance(e, Control)
             for e in obj]
        )
    )


def inplace_recurse_controls(
        action, control: Control, seen: list = None) -> None:
    """Traverse a tree of controls and perform the action.

    NOTE: This function is intended to do in-place processing, so
    actions modifying the tree itself should be made with care.
    """
    if seen is None:
        seen = []

    if id(control) in seen:
        return
    seen.append(id(control))
    action(control)

    for attr in filter(
            is_control_or_list_of, vars(control).values()):
        if isinstance(attr, Control):
            inplace_recurse_controls(action, attr, seen)

        else:
            for entry in attr:
                inplace_recurse_controls(action, entry, seen)
    return


# >>> debug_click >>>
__FLETIL__TRACE_ACTIVE = False

def __fletil__debug_click(e):
    from threading import Thread

    global __FLETIL__TRACE_ACTIVE

    if __FLETIL__TRACE_ACTIVE:
        return
    __FLETIL__TRACE_ACTIVE = True
    ctrl: flet.IconButton = e.control
    prev_color = ctrl.icon_color
    ctrl.icon_color = flet.colors.AMBER_300
    ctrl.tooltip = "Debugger active"
    ctrl.update()
    t = Thread(target=breakpoint)
    t.daemon = True
    print("\n\n!!!!!!! DEBUGGER ACTIVATED !!!!!!!")
    print('Go "up" to enter app scope, enter "e" to access the argument passed, "continue" when done.\n')
    t.run()
    __FLETIL__TRACE_ACTIVE = False
    ctrl.icon_color = prev_color
    ctrl.tooltip = "Ready"
    ctrl.update()
    print("\n\nExited debugger.")
    return
# <<< debug_click <<<


def add_dev(hor, ver, target):
    """Inject developer-assisting functionality into the page."""
    hor = "start" if hor == "left" else "end" if hor == "right" else hor
    dc_src = Path(__file__).read_text().partition("\n# >>> debug_click >>>\n")[2].partition("\n# <<< debug_click <<<\n")[0]
    t_mod = sys.modules[target.__module__]
    exec(dc_src, t_mod.__dict__)
    debug_click = t_mod.__fletil__debug_click
    row = flet.Row([
        flet.IconButton(
            flet.icons.DEVELOPER_MODE,
            icon_color=flet.colors.BLUE_GREY,
            on_click=debug_click,
            tooltip="Ready",
        ),
        flet.IconButton(
            icon=flet.icons.CIRCLE,
            icon_color=flet.colors.BLUE_GREY,
            tooltip="All good!",
            data={
                "_cid": "code_status",
                "_state_attrs": ["icon_color", "tooltip"],
            },
        )
    ], alignment=hor)

    def set_code_status(page: flet.Page, color: str, tip: str = ""):
        """Update the code status button's color and tooltip."""
        dev_buttons = getattr(page, "__fletil__dev_buttons", None)

        if not dev_buttons:
            return False
        color = color.upper()
        assert hasattr(flet.colors, color), f'invalid color "{color}"'
        button: flet.IconButton = ([
            c
            for c in dev_buttons.controls
            if (getattr(c, "data") or {}).get("_cid", "") == "code_status"] or [None])[0]

        if not button:
            return False
        button.icon_color = color
        button.tooltip = tip
        button.update()
        return True
    setattr(
        row, "set_code_status", set_code_status)

    def _add(page: flet.Page):
        target(page)

        if ver == "top":
            page.controls.insert(0, row)
        else:
            page.controls.append(row)
        setattr(page, "__fletil__dev_buttons", row)
        page.update()
        return page
    return _add
