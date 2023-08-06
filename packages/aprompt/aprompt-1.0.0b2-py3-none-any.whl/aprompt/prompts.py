from __future__ import annotations

from collections.abc import Generator, Iterable
from pathlib import Path
import string
from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    Union,
)
import warnings

import adorable
from readchar import key as Key

from .formatters import Formatter
from .utils import Display, hide_string, Pointer, swap


# type defs

T = TypeVar("T")
PromptType = Generator[str, str, tuple[T, str]]


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
) -> PromptType[str]:
    r"""
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
    formatter: Formatter = yield None # type: ignore
    display = Display()
    
    text = ""
    
    while True:
        key = yield display(formatter.prompt(
            hide_string(text) if hide else text,
        ))
        
        if key == Key.ENTER:
            return (
                text,
                display.clear() + formatter.final(hide_string(text) if hide else text)
            )
        
        elif key == Key.BACKSPACE:
            if text:
                text = text[:-1]
            
            else:
                display.alert()
        
        elif key in [Key.UP, Key.DOWN, Key.PAGE_UP, Key.PAGE_DOWN]:
            # PGUP and PGDN do not give feedback but
            # atleast it does not scroll
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

def code(
    *,
    length: int,
    hide: bool = False,
    chars: Iterable[str] = string.ascii_letters + string.digits,
    char_missing: str = "_",
    require_enter: bool = False,
) -> PromptType[str]:
    """
    Parameters
    ----------
    length
        The exact length of the code.
    
    hide
        Whether all characters should be replaced
        by asterisks when displaying.
    
    chars
        Allowed characters.
    
    char_missing
        A character that signals a missing character.
        By default this is ``_`` but if ``chars``
        contains that, this parameter should be changed.
        Otherwise a warning will be raised.
    
    require_enter
        Whether the enter key must be pressed to enter
        or the code will be entered as soon as the last
        character is pressed.
    
    Returns
    -------
    str
        The entered code.
    """
    formatter: Formatter = yield None # type: ignore
    display = Display()
    
    if char_missing in chars:
        warnings.warn("`chars` contains `char_missing`", RuntimeWarning)
    
    code = ""
    
    while True:
        key = yield display(formatter.prompt(
            (hide_string(code) if hide else code).ljust(length, char_missing)
        ))
        
        if key == Key.ENTER and require_enter and len(code) == length:
            return (
                code,
                display.clear() + formatter.final(hide_string(code) if hide else code)
            )
        
        elif key == Key.BACKSPACE:
            if code:
                code = code[:-1]
            
            else:
                display.alert()
        
        elif key in [Key.UP, Key.DOWN, Key.PAGE_UP, Key.PAGE_DOWN]:
            # PGUP and PGDN do not give feedback but
            # atleast it does not scroll
            display.alert()
        
        elif key in chars:
            code += key
            
            if not require_enter and len(code) == length:
                return (
                    code,
                    display.clear() + formatter.final(hide_string(code) if hide else code)
                )
        
        else:
            display.alert()

def sort(
    *options: str,
    sort: bool = False,
) -> PromptType[list[str]]:
    r"""
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
    formatter: Formatter = yield None # type: ignore
    display = Display(navigation = {
        "enter": SYM_ENTER,
        "select/unselect": SYM_SPACE,
        "move up": SYM_ARROW_UP,
        "move down": SYM_ARROW_DOWN,
    })
    
    if not all(options):
        raise ValueError("option cannot be empty string")
    
    optionlist: list[str] = list(options)
    
    if sort:
        optionlist = sorted(optionlist)
    
    #else:
    #    optionlist = optionlist.copy()
    
    pointer = Pointer(optionlist)
    grab_mode = False
    
    while True:
        text = []
        for idx, option in enumerate(optionlist):
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
            opts = [i for i in optionlist]
            
            return (
                opts,
                display.clear() + formatter.final(opts)
            )
        
        elif key == Key.SPACE:
            grab_mode = not grab_mode
        
        elif key == Key.UP:
            if grab_mode:
                swap(optionlist, pointer.point, pointer.up())
            
            else:
                pointer.up()
        
        elif key == Key.DOWN:
            if grab_mode:
                swap(optionlist, pointer.point, pointer.down())
            
            else:
                pointer.down()
        
        else:
            display.alert()

def select(
    *options: str,
    multiple: bool = False,
    sort: bool = False,
    require: Union[Iterable[int], Callable[[int], bool], int, None] = None,
) -> PromptType[Union[list[str], str]]:
    r"""
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
        This may also be a callable taking one argument
        (the amount of selected options) that returns either
        ``True`` to continue or ``False`` to signal, that the
        amount is invalid. This would be equal to specifying
        the `repeat_while` parameter in the main prompt function
        with the difference that it does not reset the selected
        options.
    
    Returns
    -------
    list[str]
        Selected options if ``multiple`` is enabled.
    
    str
        Selected option if ``multiple`` is disabled.
    """
    formatter: Formatter = yield None # type: ignore
    display = Display(navigation = {
        "enter": SYM_ENTER,
        **({"select/unselect": SYM_SPACE} if multiple else {}),
        "move up": SYM_ARROW_UP,
        "move down": SYM_ARROW_DOWN,
    })
    
    if require is not None and not multiple:
        raise ValueError("`require` is set but `mutiple` is not enabled")
    
    if not all(options):
        raise ValueError("option cannot be empty string")
    
    if sort:
        options = tuple(sorted(options))
    
    pointer = Pointer(options)
    selected: list[int] = []
    
    while True:
        text: list[str] = []
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
                
                if require is not None:
                    success = False
                
                    if callable(require):
                        if require(len(chose)):
                            success = True
                    
                    elif isinstance(require, int):
                        success = len(chose) == require
                    
                    elif len(chose) in require:
                        success = True
                    
                    if not success:
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
) -> PromptType[int]:
    r"""
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
    formatter: Formatter = yield None # type: ignore
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
) -> PromptType[bool]:
    r"""
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
    formatter: Formatter = yield None # type: ignore
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

def path(
    root: Union[Path, str, None] = None,
    *,
    allow_creation: bool = False,
    require_file: bool = False,
    multiple_files: bool = False,
) -> PromptType[Union[list[Path], Path]]:
    r"""
    Parameters
    ----------
    root
        Directory the user, where the user starts
        navigating. Defaults to current working
        directory.
    
    allow_creation
        Allows the creation of directories or files
        respectively. Note that only the directories
        that are required will be created and only after
        the user hits enter.
    
    require_file
        By default the user is prompted to select
        a directory. Be enabling this option, the
        a file is requires to be selected.
    
    multiple_files
        If ``require_file`` is enabled, this will
        allow selecting multiple files.
    
    Returns
    -------
    list[Path]
        List of path objects, when ``multiple_files``
        is enabled.
    
    Path
        The selected directory or file as a path
        object.
    """
    formatter: Formatter = yield None # type: ignore
    display = Display(navigation = {
        "enter": SYM_ENTER,
        "open directory": SYM_SPACE,
        "goto parent directory": SYM_ARROW_LEFT,
        #"goto root directory": "",
    })
    
    current_path = Path(root or Path.cwd()).resolve()
    selected: list[int] = []
    options = list(current_path.iterdir())
    pointer = Pointer(options)
    
    while True:
        tree = []
        for idx, d in enumerate(options):
            #d = directory.name
            
            apply = formatter.option
            
            if d in selected:
                apply = formatter.check
            
            elif multiple_files:
                apply = formatter.uncheck
            
            if idx == pointer.point:
                tree.append(apply(formatter.select(formatter.path(d))))
            
            else:
                tree.append(apply(formatter.unselect(formatter.path(d))))
        
        key = yield display(
            str(current_path) + "/\n",
            *tree,
            ", ".join(map(str, selected))
        )
        
        if key == Key.ENTER:
            if multiple_files:
                ...
            
            else:
                p = pointer.get()
                if p.is_file() == require_file:
                    return (
                        p,
                        display.clear() + formatter.final(p)
                    )
                
                display.alert()
        
        elif key == Key.SPACE:
            p = pointer.get()
            if p.is_dir():
                current_path /= p
                
                options = list(current_path.iterdir())
                pointer = Pointer(options)
            
            else:
                display.alert()
        
        elif key == Key.UP:
            pointer.up()
        
        elif key == Key.DOWN:
            pointer.down()
        
        elif key == Key.LEFT:
            current_path = current_path.parent
            
            options = list(current_path.iterdir())
            pointer = Pointer(options)
        
        else:
            display.alert()
