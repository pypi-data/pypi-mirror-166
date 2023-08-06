from abc import ABC, abstractmethod
from pathlib import Path
from time import struct_time
from typing import Any

from .utils import color, fill, horizontal_line


class Formatter(ABC):
    @staticmethod
    @abstractmethod
    def adjust_number(_: int) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def ask(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def check(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def confirm(_: bool) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def datetime(_: struct_time) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def final(_: Any) -> str:
        ...
    
    
    @staticmethod
    @abstractmethod
    def grab(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def option(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def path(_: Path) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def prompt(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def select(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def selected_files(_: list[Path]) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def uncheck(_: str) -> str:
        ...
    
    @staticmethod
    @abstractmethod
    def unselect(_: str) -> str:
        ...


class ColoredFormatter(Formatter):
    @staticmethod
    def adjust_number(value: int) -> str:
        return f"+ {value:>3} -\n"
    
    @staticmethod
    def ask(value: str) -> str:
        return fill(
            value,
            prepend = color("? ", "green"),
        ) + "\n"
    
    @staticmethod
    def check(value: str) -> str:
        return fill(
            value,
            prepend = color("\N{CHECK MARK} ", "green")
        ) + "\n"
    
    @staticmethod
    def confirm(value: bool) -> str:
        y, n = ("Y", "n") if value else ("y", "N")
        return f": [{y}/{n}]\n"
    
    @staticmethod
    def datetime(value: struct_time) -> str:
        ...
    
    @staticmethod
    def final(value: Any) -> str:
        if isinstance(value, list):
            if all(isinstance(i, Path) for i in value):
                value = "\n".join(map(str, value))
            
            else:
                value = ", ".join(map(str, value))
        
        return fill(
            value,
            prepend = color("~ ", "yellow")
        ) + "\n"
    
    @staticmethod
    def grab(value: str) -> str:
        return fill(
            value,
            prepend = color("> ", "yellow")
        ) + "\n"
    
    @staticmethod
    def option(value: str) -> str:
        return f"  {value}"
    
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
    def prompt(value: str) -> str:
        return fill(
            value,
            prepend = color(": ", "yellow"),
        ) + "\n"
    
    @staticmethod
    def select(value: str) -> str:
        return f"{color(value, 'yellow')}\n"
    
    @staticmethod
    def selected_files(value: list[Path]) -> str:
        if not value:
            return ""
        
        return "".join(fill(file, prepend = "- ") + "\n" for file in value)
    
    @staticmethod
    def uncheck(value: str) -> str:
        return fill(
            value,
            prepend = color("\N{MULTIPLICATION SIGN} ", "red")
        ) + "\n"
    
    @staticmethod
    def unselect(value: str) -> str:
        return f"{value}\n"


#class BasicFormatter(Formatter):
#    ...


#class EmojiFormatter(Formatter):
#    ...

