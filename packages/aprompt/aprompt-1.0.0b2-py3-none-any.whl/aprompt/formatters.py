from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import adorable

from .utils import color, fill


class Formatter(ABC):
    @staticmethod
    @abstractmethod
    def ask(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def grab(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def final(_: Any) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def prompt(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def path(_: Path) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def adjust_number(_: int) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def select(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def unselect(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def option(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def check(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def uncheck(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def confirm(_: bool) -> str:
        ...

class ColoredFormatter(Formatter):
    @staticmethod
    def ask(value: str) -> str:
        prefix = color("? ", "green")
        return fill(
            value,
            prepend = prefix,
        ) + "\n"
    
    @staticmethod
    def prompt(value: str) -> str:
        return f"{color(':', 'yellow')} {value}{adorable.INVERSE(' ')}\n"
    
    @staticmethod
    def path(value: Path) -> str:
        if value.is_dir():
            return "\N{FILE FOLDER} " + value.name
        
        elif value.is_symlink():
            return "\N{LINK SYMBOL} " + value.name
        
        elif value.is_file():
            return "\N{PAGE FACING UP} " + value.name
        
        else:
            return f"  {value}"
    
    @staticmethod
    def grab(value: str) -> str:
        return color(f"> {value}", "yellow") + "\n"
    
    @staticmethod
    def final(value: Any) -> str:
        if isinstance(value, list):
            if all(isinstance(i, str) for i in value):
                value = ", ".join(value)
        
        return f"{color('~', 'yellow')} {value}\n"
    
    @staticmethod
    def adjust_number(value: int) -> str:
        return f"+ {value:>3} -\n"
    
    @staticmethod
    def select(value: str) -> str:
        return f"{color(value, 'yellow')}\n"
    
    @staticmethod
    def unselect(value: str) -> str:
        return f"{value}\n"
    
    @staticmethod
    def option(value: str) -> str:
        return f"  {value}"
    
    @staticmethod
    def check(value: str) -> str:
        return color("\N{CHECK MARK}", "green") + f" {value}"
    
    @staticmethod
    def uncheck(value: str) -> str:
        return color("\N{MULTIPLICATION SIGN}", "red") + f" {value}"
    
    @staticmethod
    def confirm(value: bool) -> str:
        y: str
        n: str
        
        y, n = ("Y", "n") if value else ("y", "N")
        return f": [{y}/{n}]\n"
    