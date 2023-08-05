from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
import string
from typing import (
    Any,
    Generator,
    Optional,
    Union,
)

import adorable
from readchar import key as Key

from .utils import Display, Pointer, swap


# type defs

PromptType = Generator[str, str, Any]


# symbol defs

SYM_ARROW_UP = "\N{UPWARDS ARROW}"
SYM_ARROW_DOWN = "\N{DOWNWARDS ARROW}"
SYM_ARROW_LEFT = "\N{LEFTWARDS ARROW}"
SYM_ARROW_RIGHT = "\N{RIGHTWARDS ARROW}"

SYM_ENTER = "\N{RETURN SYMBOL}"
SYM_BACKSPACE = "\N{ERASE TO THE LEFT}"
SYM_SPACE = "Space"


# other defs

SPACE = " \t"


# prompt defs

def text(
    *,
    hide: bool = False,
    allow_any: bool = False,
) -> PromptType:
    """
    Parameters
    ----------
    hide
        Whether all characters should be replaced
        by asterisks when displaying.
    
    allow_any
        If set to ``False``, only alphanumeric,
        punctuation and spaces are allowed to type.
    
    Returns
    -------
    str
        The entered text.
    
    """
    formatter = yield
    display = Display()
    
    text = ""
    
    while True:
        key = yield display(formatter.prompt(
            "*" * len(text) if hide else text,
        ))
        
        if key == Key.ENTER:
            return (
                text,
                display.clear() + ("" if hide else formatter.final(text))
            )
        
        elif key == Key.BACKSPACE:
            if text:
                text = text[:-1]
            
            else:
                display.alert()
        
        elif allow_any:
            if (
                key.isalnum()
                or key in string.punctuation
                or key in SPACE
            ):
                text += key
            
            else:
                display.alert()
        
        else:
            text += key

def sort(
    *options: str,
    sort: bool = False,
) -> PromptType:
    """
    Parameters
    ----------
    options
        Options to choose from.
    
    sort
        Sort options by built-in ``sorted`` function.
    
    Returns
    -------
    list[str]
        Provides options, but resorted.
    """
    formatter = yield
    display = Display(navigation = {
        "enter": SYM_ENTER,
        "select/unselect": SYM_SPACE,
        "move up": SYM_ARROW_UP,
        "move down": SYM_ARROW_DOWN,
    })
    
    if not all(options):
        raise ValueError("option cannot be empty string")
    
    if sort:
        options = sorted(options)
    
    else:
        options = options.copy()
    
    pointer = Pointer(options)
    grab_mode = False
    
    while True:
        text = []
        for idx, option in enumerate(options):
            if idx == pointer.point:
                if grab_mode:
                    text.append(formatter.grab(option))
                
                else:
                    text.append(formatter.select(formatter.option(option)))
            
            else:
                text.append(formatter.unselect(formatter.option(option)))
        
        key = yield display(
            *text
        )
        
        if key == Key.ENTER:
            opts = [i for i in options]
            
            return (
                opts,
                display.clear() + formatter.final(opts)
            )
        
        elif key == Key.SPACE:
            grab_mode = not grab_mode
        
        elif key == Key.UP:
            if grab_mode:
                swap(options, pointer.point, pointer.up())
            
            else:
                pointer.up()
        
        elif key == Key.DOWN:
            if grab_mode:
                swap(options, pointer.point, pointer.down())
            
            else:
                pointer.down()
        
        else:
            display.alert()

def select(
    *options: str,
    multiple: bool = False,
    sort: bool = False,
    require: Optional[Iterable[int], int] = None,
) -> PromptType:
    """
    Parameters
    ----------
    options
        Options to choose from.
    
    multiple
        Whether only one or multple options can
        be selected.
    
    sort
        Sort options by built-in ``sorted`` function.
    
    require
        ``int`` or iterable of ``int``\s (e. g. ``range``
        or ``itertools.count``) indicating the amount of
        options that can be selected. Setting this parameter
        requires enabling ``multiple``.
    
    Returns
    -------
    list[str]
        Selected options if ``multiple`` is enabled.
    
    str
        Selected option if ``multiple`` is disabled.
    """
    formatter = yield
    display = Display(navigation = {
        "enter": SYM_ENTER,
        **({"select/unselect": SYM_SPACE} if multiple else {}),
        "move up": SYM_ARROW_UP,
        "move down": SYM_ARROW_DOWN,
    })
    
    if require is not None and not multiple:
        raise ValueError("require is set but mutiple is not enabled")
    
    if not all(options):
        raise ValueError("option cannot be empty string")
    
    if sort:
        options = sorted(options)
    
    pointer = Pointer(options)
    selected = []
    
    while True:
        text = []
        for idx, option in enumerate(options):
            apply = lambda x: x
            
            if idx in selected:
                apply = formatter.check
            
            elif multiple:
                apply = formatter.uncheck
            
            if idx == pointer.point:
                opt = formatter.select(option)
            
            else:
                opt = formatter.unselect(option)
            
            text.append(apply(opt))
        
        key = yield display(
            *text
        )
        
        if key == Key.ENTER:
            if multiple:
                chose = [options[i] for i in selected]
                
                if require is not None and len(chose) not in require:
                    display.alert()
                    continue
                
                return (
                    chose,
                    display.clear() + formatter.final(", ".join(chose))
                )
            
            return (
                pointer.get(),
                display.clear() + formatter.final(pointer.get())
            )
        
        elif key == Key.SPACE and multiple:
            if pointer.point in selected:
                selected.remove(pointer.point)
            
            else:
                selected.append(pointer.point)
        
        elif key == Key.UP:
            pointer.up()
        
        elif key == Key.DOWN:
            pointer.down()
        
        else:
            display.alert()

def amount(
    *,
    default: int = 0,
    factor: int = 1,
    maximum: Optional[int] = None,
    minimum: Optional[int] = None,
) -> PromptType:
    """
    Parameters
    ----------
    default
        Integer to start at. Must be between ``maximum``
        and ``minimum`` in case they are defined. This
        can be any int-like number, that provides the
        ``__iadd__``, ``__isub__`` and ``__int__`` methods.
    
    factor
        Integer indicating by how much the value should
        be increased/decreased.
    
    maximum
        Integer the value cannot exceed. When the value
        is not the maximum but the factor would make the
        value go above, the value stays the same. By default,
        there is no maximum value.
    
    minimum
        Same as ``maximum`` but with an integer the value
        cannot fall below.
    
    Returns
    -------
    int
        The adjusted value.
    """
    formatter = yield
    display = Display(navigation = {
        "enter": SYM_ENTER,
        "increase": [SYM_ARROW_UP, "+"],
        "decrease": [SYM_ARROW_DOWN, "-"],
    })
    
    value = default
    
    while True:
        key = yield display(
            formatter.adjust_number(value)
        )
        
        if key == Key.ENTER:
            return (
                value,
                display.clear() + formatter.final(value)
            )
        
        elif key in [Key.UP, "+"]:
            value += factor
            if maximum is not None and value > maximum:
                value -= factor
                display.alert()
        
        elif key in [Key.DOWN, "-"]:
            value -= factor
            if minimum is not None and value < minimum:
                value += factor
                display.alert()
        
        else:
            display.alert()

def confirm(
    *,
    default: bool = True
) -> PromptType:
    """
    Parameters
    ----------
    default
        If the user does not type any value,
        this is going to be used.
    
    Returns
    -------
    bool
        The answer.
    """
    formatter = yield
    display = Display(navigation = {
        "enter": SYM_ENTER,
        "yes": "Y y",
        "no": "N n",
    })
    
    while True:
        key = yield display(
            formatter.confirm(default)
        )
        
        if key == Key.ENTER:
            return (
                bool(default),
                display.clear() + formatter.final("y" if default else "n")
            )
        
        elif key in "Yy":
            return (
                True,
                display.clear() + formatter.final("y")
            )
        
        elif key in "Nn":
            return (
                False,
                display.clear() + formatter.final("n")
            )
        
        else:
            display.alert()

#def path(
#    root: Optional[Path, str] = None,
#    *,
#    allow_creation: bool = False,
#    require_file: bool = False,
#    multiple_files: bool = False,
#) -> PromptType:
#    """
#    Parameters
#    ----------
#    root
#        Directory the user, where the user starts
#        navigating. Defaults to current working
#        directory.
#    
#    allow_creation
#        Allows the creation of directories or files
#        respectively. Note that only the directories
#        that are required will be created and only after
#        the user hits enter.
#    
#    require_file
#        By default the user is prompted to select
#        a directory. Be enabling this option, the
#        a file is requires to be selected.
#    
#    multiple_files
#        If ``require_file`` is enabled, this will
#        allow selecting multiple files.
#    
#    Returns
#    -------
#    list[Path]
#        List of path objects, when ``multiple_files``
#        is enabled.
#    
#    Path
#        The selected directory or file as a path
#        object.
#    """
#    formatter = yield
#    display = Display(navigation = {
#        "enter": SYM_ENTER,
#        "open directory": SYM_SPACE,
#        "goto parent directory": SYM_ARROW_LEFT,
#        "goto root directory": ""
#    })
#    
#    current_path = Path(root or Path.cwd()).resolve()
#    selected = []
#    options = list(current_path.iterdir())
#    pointer = Pointer(options)
#    
#    while True:
#        tree = []
#        for idx, d in enumerate(options):
#            #d = directory.name
#            
#            apply = formatter.option
#            
#            if d in selected:
#                apply = formatter.check
#            
#            elif multiple_files:
#                apply = formatter.uncheck
#            
#            if idx == pointer.point:
#                tree.append(apply(formatter.select(formatter.path(d))))
#            
#            else:
#                tree.append(apply(formatter.unselect(formatter.path(d))))
#        
#        key = yield display(
#            str(current_path) + "/\n",
#            *tree,
#            ", ".join(map(str, selected))
#        )
#        
#        if key == Key.ENTER:
#            if multiple_files:
#                ...
#            
#            else:
#                p = pointer.get()
#                if p.is_file() == require_file:
#                    return (
#                        p,
#                        display.clear() + formatter.final(p)
#                    )
#                
#                display.alert()
#        
#        elif key == Key.SPACE:
#            p = pointer.get()
#            if p.is_dir():
#                current_path /= p
#                
#                options = list(current_path.iterdir())
#                pointer = Pointer(options)
#            
#            else:
#                display.alert()
#        
#        elif key == Key.UP:
#            pointer.up()
#        
#        elif key == Key.DOWN:
#            pointer.down()
#        
#        elif key == Key.LEFT:
#            current_path = current_path.parent
#            
#            options = list(current_path.iterdir())
#            pointer = Pointer(options)
#        
#        else:
#            display.alert()
#