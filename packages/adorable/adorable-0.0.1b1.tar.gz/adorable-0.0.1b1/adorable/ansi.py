from __future__ import annotations

from abc import ABC
from sys import stdout
from typing import Any, Optional, Sequence


class Ansi(ABC):
    def __str__(self):
        return self.enable_str()
    
    def __call__(self, *args, **kwargs):
        return paint(*args, style = self, **kwargs)
    
    def enable_str(self) -> str:
        return get_ansi_string(*self._ansi)
    
    def enable(self, file = stdout) -> None:
        file.write(self.enable_str())
    
    def disable_str(self) -> str:
        return get_ansi_string(*self._off)
    
    def disable(self, file = stdout) -> None:
        file.write(self.disable_str())

class AnsiNull(Ansi):
    def __init__(self):
        self._ansi = []
        self._off = []

def get_ansi_string(*args):
    return f"\x1b[{';'.join(map(str, args))}m"

def paint(*args: Any, style: Optional[Ansi] = None, sep: str = " ") -> str:
    content = sep.join(map(str, args))
    
    if style is None:
        return content
    
    elif not isinstance(style, Ansi):
        raise TypeError(f"expected `None`, `Ansi` for argument `style`, got {style.__class__.__name__}")
    
    return f"{style}{content}{style.disable_str()}"

def printc(*args: Any, **kwargs: Any) -> None:
    paint_kwargs = {}
    
    for key in ["style", "sep"]:
        if key in kwargs:
            paint_kwargs[key] = kwargs.pop(key)
    
    print(paint(*args,
        **paint_kwargs
    ), **kwargs)
