from .ansi import Ansi, get_ansi_string

class Style(Ansi):
    def __init__(self, enable, disable):
        self._ansi = [enable]
        self._off = [disable]

BOLD = Style(1, 22)          # b
DIM = Style(2, 22)           # d
ITALIC = Style(3, 23)        # i
UNDERLINE = Style(4, 24)     # u
BLINK = Style(5, 25)         # f (flash)
INVERSE = Style(7, 27)       # r (reverse)
INVISIBLE = Style(8, 28)     # h (hidden)
STRIKETHROUGH = Style(9, 29) # s
