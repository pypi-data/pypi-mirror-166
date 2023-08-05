from __future__ import annotations

from abc import ABCMeta, abstractmethod
from copy import copy
from enum import auto, IntEnum
import operator
from typing import Callable, Sequence, Union

from . import _ansi_conv
from . import webcolors
from .ansi import Ansi, get_ansi_string
from .style import Style
from .term import Terminal
from .utils import get_closest_color,  RGB, HEX, T_RGB


NOT_INITIALISED: str = "color not initialised"
ALREADY_INITIALISED: str = "color already initialised"


class GroundError(Exception):
    pass


class Ground(IntEnum):
    NONE = auto()
    FORE = auto()
    BACK = auto()
    BOTH = auto()
    
    @staticmethod
    def check(*checks: Sequence[Callable, Union[Color, Ground], ...], msg: str = "invalid ground set") -> None:
        for check in checks:
            args = []
            for arg in check[1:]:
                if isinstance(arg, Color):
                    args.append(arg._ground)
                
                elif isinstance(arg, str):
                    msg = arg
                
                elif isinstance(arg, int):
                    args.append(arg)
                
                else:
                    raise TypeError(f"expected 'Color', 'int' or 'str', got {arg.__class__.__name__!r}")
            
            if not check[0](*args):
                raise GroundError(msg)

class Color(Ansi, metaclass = ABCMeta):
    """
    Abstract Base Class for terminal dependent
    colors
    """
    def __init__(self, **data):
        self._ansi = []
        self._off = [0]
        self._data  = data
        self._ground = Ground.NONE
    
    def __repr__(self):
        return f"{self.__class__.__name__}"
    
    def __str__(self):
        if self._ground == Ground.NONE:
            return f"{self.__class__.__name__} (not initialised)"
        
        return self.enable_str()
    
    def __add__(self, other: Ansi):
        """
        Combines two styles.
        
        Raises
        ------
        ValueError
            Colors cannot be combined.
        """
        if isinstance(other, Color):
            Ground.check([
                operator.ne,
                other, Ground.NONE,
                NOT_INITIALISED
            ], [
                operator.ne,
                other, self,
                "both colors are set to the same ground"
            ])
        
        elif not isinstance(other, Ansi):
            return NotImplemented
        
        obj = copy(self)
        obj.extend(other)
        
        return obj
    
    def __iadd__(self, other: Ansi):
        """
        Combines two styles.
        
        Raises
        ------
        ValueError
            Colors cannot be combined.
        """
        if isinstance(other, Color):
            Ground.check([
                operator.ne,
                other, Ground.NONE,
                NOT_INITIALISED
            ], [
                operator.ne,
                other, self,
                "both colors are set to the same ground"
            ])
        
        elif not isinstance(other, Ansi):
            return NotImplemented
        
        self.extend(other)
        
        return self
    
    def __call__(self, *args: Any, **kwargs: Any):
        Ground.check([
            operator.ne,
            self, Ground.NONE,
            NOT_INITIALISED
        ])
        
        return paint(*args, style = self, **kwargs)
    
    def extend(self, other: Ansi):
        self._ansi.extend(other._ansi)
        self._off.extend(other._off)
        return self
    
    def _get_ansi(self) -> str:
        return get_ansi_string(self._ansi)
    
    @abstractmethod
    def _form(self, ground: Ground) -> list[Any]:
        ...
    
    @property
    def fg(self):
        Ground.check([
            operator.eq,
            self, Ground.NONE,
            ALREADY_INITIALISED
        ])
        
        self._ansi.extend(self._form(Ground.FORE))
        self._ground = Ground.FORE
        
        return self
    
    @property
    def bg(self):
        Ground.check([
            operator.eq,
            self, Ground.NONE,
            ALREADY_INITIALISED
        ])
        
        self._ansi.extend(self._form(Ground.BACK))
        self._ground = Ground.BACK
        
        return self
    
    def on(self, other: Color):
        Ground.check([
            lambda a, b, back, fore: a != back and b != fore,
            self, other, Ground.BACK, Ground.FORE,
            "second color must not be set to background"
        ])
        
        self = self.fg
        self.extend(other.bg if other._ground != Ground.BACK else other)
        
        self._ground = Ground.BOTH
        
        return self
    
    @classmethod
    @abstractmethod
    def from_rgb(cls, rgb: RGB):
        ...
    
    @classmethod
    def from_name(cls, name: str):
        return cls.from_rgb(webcolors.colors[name.lower()])
    
    @classmethod
    def from_hex(cls, hex: HEX):
        if isinstance(hex, int):
            # convert to string
            hex = f"{hex:X}"
            
            # leading 0s will be removed so we need
            # to add them
            if len(hex) < 3:
                hex = hex.zfill(3)
            
            elif len(hex) < 6:
                hex = hex.zfill(6)
        
        if not isinstance(hex, str):
            raise TypeError("hex value must be int or str")
        
        hex = hex.removeprefix("#")
        
        if len(hex) == 3:
            # convert to a six chars long string
            hex = "".join(char * 2 for char in hex)
        
        elif len(hex) != 6:
            raise ValueError(f"hex must be 3 or 6 characters long")
        
        h = iter(hex)
        
        rgb = [int(char, 16) * 16 + int(next(h), 16) for char in h]
        return cls.from_rgb(rgb)

class Color0bit(Color):
    _termtype = Terminal.NOCOLOR
    
    def _form(self, ground: Ground):
        return []
    
    @classmethod
    def from_rgb(cls, rgb: T_RGB):
        return cls()

class Color3bit(Color):
    _termtype = Terminal.BIT3
    
    def _form(self, ground: Ground):
        value = self._data["ansi"]
        
        if ground in [Ground.NONE, Ground.BOTH]:
            raise ValueError()
        
        return [
            30 + value
        ]
    
    @classmethod
    def from_rgb(cls, rgb: T_RGB):
        color = get_closest_color(RGB(*rgb), enumerate(_ansi_conv.ANSI3BIT))
        return cls(ansi = color)


class Color4bit(Color):
    _termtype = Terminal.BIT4
    
    def _form(self, ground: Ground):
        value = self._data["ansi"]
        
        if ground in [Ground.NONE, Ground.BOTH]:
            raise ValueError()
        
        return [
            
        ]
    
    @classmethod
    def from_rgb(cls, rgb: RGB):
        color = get_closest_color(RGB(*rgb), enumerate(_ansi_conv.ANSI4BIT))
        return cls(ansi = color)


class Color8bit(Color):
    _termtype = Terminal.BIT8
    
    def _form(self, ground: Ground):
        value = self._data["ansi"]
        
        if ground in [Ground.NONE, Ground.BOTH]:
            raise ValueError()
        
        return [
            38 if ground == Ground.FORE else 48,
            5,
            value
        ]
    
    @classmethod
    def from_rgb(cls, rgb: RGB):
        color = get_closest_color(RGB(*rgb), enumerate(_ansi_conv.ANSI8BIT))
        return cls(ansi = color)

class Color24bit(Color):
    _termtype = Terminal.BIT24
    
    def _form(self, ground: Ground):
        r, g, b = self._data["rgb"]
        
        if ground in [Ground.NONE, Ground.BOTH]:
            raise ValueError()
        
        return [
            38 if ground == Ground.FORE else 48,
            2,
            r, g, b
        ]
    
    @classmethod
    def from_rgb(cls, rgb: RGB):
        return cls(rgb = rgb)

def get_color():
    t = Terminal.get_term()
    
    for colortype in [Color0bit, Color3bit, Color4bit, Color8bit, Color24bit]:
        if colortype._termtype == t:
            return colortype
    
    raise RuntimeError(f"could not get color with terminal type {t}")

def from_hex(*args, **kwargs):
    col = get_color()
    return col.from_hex(*args, **kwargs)

def from_rgb(*args, **kwargs):
    col = get_color()
    return col.from_rgb(*args, **kwargs)

def from_name(*args, **kwargs):
    col = get_color()
    return col.from_name(*args, **kwargs)

def paint(*args, style = None, sep = " ") -> str:
    content = sep.join(map(str, args))
    
    if style is None:
        return content
    
    elif not isinstance(style, Ansi):
        raise TypeError(f"expected `None`, `Ansi` for argument `style`, got {style.__class__.__name__}")
    
    return f"{style}{content}{style.disable_str()}"

def printc(*args, **kwargs) -> None:
    print(paint(*args,
        style = kwargs.pop("style", None),
        sep = kwargs.pop("sep", " ")
    ), **kwargs)