from enum import auto, IntEnum
import os
import sys

class Terminal(IntEnum):
    NOCOLOR = auto()
    BIT3 = auto()
    BIT4 = auto()
    BIT8 = auto()
    BIT24 = auto()
    
    @classmethod
    def get_term(cls):
        if not (sys.stdout and sys.stdout.isatty()):
            raise RuntimeError("standard output is not a valid terminal")
        
        ac = os.getenv("ADORABLE_COLOR", None)
        if ac == "nocolor":
            return cls.NOCOLOR
        
        if ac == "3bit":
            return cls.BIT3
        
        if ac == "4bit":
            return cls.BIT4
        
        if ac == "8bit":
            return cls.BIT8
        
        if ac == "24bit":
            return cls.BIT24
        
        if int(os.getenv("NO_COLOR", "0")):
            return cls.NOCOLOR
        
        if os.getenv("COLORTERM", "0") in ["truecolor", "24bit"]:
            return cls.BIT24
        
        t = os.getenv("TERM", "").removeprefix("xterm-")
        if t == "256":
            return cls.BIT8
        
        return cls.NOCOLOR