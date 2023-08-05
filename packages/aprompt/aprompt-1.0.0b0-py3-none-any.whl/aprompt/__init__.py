from __future__ import annotations

import signal
import sys
from typing import (
    Any,
    Callable,
    IO,
    Optional,
)

from readchar import readkey, key as Key

from .formatters import Formatter, ColoredFormatter
from .prompts import PromptType

def prompt(
    message: str,
    kind: PromptType,
    *,
    repeat_while: Callable[[Any], bool] | bool = False,
    cleanup: Optional[Callable[[], None]] = None,
    file: Optional[IO] = None,
    formatter: Formatter = ColoredFormatter,
) -> Any:
    """
    Parameters
    ----------
    message
    kind
        The kind of prompt to use. Select one
        from the :module:`prompts` module or
        `a custom defined one`.
    
    repeat_while
        A callable that takes the prompt's result
        as an argument and returns whether the
        prompt should be repeated.
        
    cleanup
        A callable that will be called when the
        user hits Ctrl-C during a prompt. After
        that, the programm will be terminated.
    
    file
        A file to write to. Usually ``sys.stdout``
        or ``sys.stderr``. Defaults to ``sys.stdout``.
    
    Returns
    -------
    The prompt's return value.
    """
    if file is None:
        file = sys.stdout
    
    file.write(formatter.ask(message))
    file.flush()
    
    next(kind)
    text = kind.send(formatter)
    
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
        res, post = result.value
        if post is not None:
            file.write(post + "\n")
            file.flush()
        
        return res
    
    raise RuntimeError(f"{kind.__name__!r} never returned anything")
