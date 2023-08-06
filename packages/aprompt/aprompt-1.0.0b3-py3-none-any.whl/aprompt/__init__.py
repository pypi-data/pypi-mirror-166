from __future__ import annotations

import signal
import sys
from typing import (
    Any,
    Callable,
    Optional,
    TextIO,
    TypeVar,
)

from readchar import readkey, key as Key

from .formatters import Formatter, ColoredFormatter
from .prompts import T, PromptType


#T = TypeVar("T")


def prompt(
    message: str,
    kind: PromptType[T],
    *,
    cleanup: Optional[Callable[[], None]] = None,
    file: Optional[TextIO] = None,
    formatter: Optional[Formatter] = None,
) -> T:
    """
    Parameters
    ----------
    message
        The message/question to display.
    
    kind
        The kind of prompt to use. Select one
        from the :mod:`prompts` module or
        `a custom defined one`.
    
    cleanup
        A callable that will be called when the
        user hits Ctrl-C during a prompt. After
        that, the programm will be terminated.
    
    file
        A file to write to. Usually ``sys.stdout``
        or ``sys.stderr``. Defaults to ``sys.stdout``.
    
    formatter
        A :class:`Formatter` that formats the prompt.
        Defaults to :class:`formatters.ColoredFormatter`.
    
    Returns
    -------
    The prompt's return value.
    """
    if file is None:
        file = sys.stdout
    
    if formatter is None:
        formatter = ColoredFormatter()
    
    file.write(formatter.ask(message))
    file.flush()
    
    next(kind)
    text = kind.send(formatter) # type: ignore
    
    try:
        while True:
            file.write(text)
            file.flush()
            
            key = readkey()
            
            if key == Key.CTRL_C:
                if cleanup is not None:
                    cleanup()
                
                sys.exit(signal.SIGINT)
            
            text = kind.send(key)
    
    except StopIteration as result:
        if result is None:
            raise RuntimeError(f"{kind.__name__!r} never returned anything")
        
        res, post = result.value
        
        if post is not None:
            file.write(post + "\n")
            file.flush()
        
        return res
