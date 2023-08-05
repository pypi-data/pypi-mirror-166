from collections.abc import Iterator, Mapping
from shutil import get_terminal_size
import ansiwrap
from typing import (
    Any,
    Union,
)

from adorable import Color3bit

def twidth() -> int:
    return get_terminal_size().columns

def swap(l: list, a: int, b: int) -> None:
    l[a], l[b] = l[b], l[a]

def color(text: str, c: str) -> str:
    return Color3bit.from_name(c).fg(text)

def horizontal_line() -> str:
    return "\N{EM DASH}" * twidth()

def clear_lines(amount: int) -> str:
    return "\x1b[1A\x1b[2K\r" * amount

class Pointer:
    def __init__(self, options: Iterator[Any]):
        self._options = options
        self._max_idx = len(options) - 1
        self.point = 0
    
    def get(self) -> Any:
        return self._options[self.point]
    
    def down(self) -> int:
        if self.point == self._max_idx:
            self.point = 0
            return self.point
        
        self.point += 1
        return self.point
    
    def up(self) -> int:
        if self.point == 0:
            self.point = self._max_idx
            return self.point
        
        self.point -= 1
        return self.point

class Display:
    def __init__(self, navigation: Mapping[str, Union[str | list[str]]] = {}):
        nav = {"quit": "Ctrl-C"} | navigation
        self.navstr = "Navigation\n"
        
        for action, keys in nav.items():
            if isinstance(keys, str):
                keys = keys.split()
           
            self.navstr += f"  {action}    {'  '.join(keys)}\n"
        
        self.rows = 0
        self.ring = False
    
    def __call__(
        self,
        *messages: str,
        seperate: bool = False
    ) -> str:
        text = "".join([
            self.clear(),
            "\a" if self.ring else "",
            ansiwrap.fill(
                ("\n" if seperate else "").join(messages),
                width = twidth(),
                replace_whitespace = False,
                drop_whitespace = False,
            ),
            horizontal_line(),
            self.navstr
        ])
        
        self.rows = text.count("\n") + 1
        self.ring = False
        
        return text
    
    def clear(self) -> str:
        return clear_lines(self.rows)
    
    def alert(self) -> None:
        self.ring = True

