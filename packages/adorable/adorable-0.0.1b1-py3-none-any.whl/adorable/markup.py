from __future__ import annotations

__all__ = ["markup"]

import html
import string
from typing import Any, Iterator, Sequence, Optional
import xml.etree.ElementTree as ET


from .ansi import Ansi, AnsiNull

class XMLEscapeFormatter(string.Formatter):
    """
    If conversion specifier 'e' (escape) is
    given or omitted, escape xml contents of
    the value. If 'r' (raw) is given, insert
    without escaping.
    """
    
    @staticmethod
    def convert_field(value, conversion):
        if conversion in ["e", None]:
            return html.escape(value)
        
        elif conversion == "r":
            return value
        
        raise ValueError(f"Unknown conversion specifier {conversion}")

def get_ansi_from_tag(name: str, style: dict[str, Ansi] = {}) -> Ansi:
    if name in style:
        return style[name]
    
    raise ValueError(f"invalid tag {name!r}")

def style_element(
    element: ET.Element,
    style: dict[str, Ansi] = {},
    _previous_ansi: Ansi = AnsiNull(),
) -> str:
    """
    Yields
    ------
    Text snippets.
    """
    for child in element:
        tag = child.tag
        ansi = get_ansi_from_tag(tag, style = style)
        
        yield ansi.enable_str() + (child.text or "")
        
        yield from style_element(
            child,
            style = style,
            _previous_ansi = ansi
        )
        
        yield (
            ansi.disable_str() +
            _previous_ansi.enable_str() +
            (child.tail or "")
        )
    
    #? yield _previous_ansi.disable_str()

def markup(
    string: str,
    args: Sequence[Any] = [],
    kwargs: dict[str, Any] = {},
    style: Optional[dict[str, Ansi]] = None
) -> str:
    """
    Use XML to style a string. In order to
    format the string, provide the variables
    directly to this function. All variables
    will be escaped automatically unless ``!r``
    is added at the end. You can also use ``!e``
    to explicitly specify that the variable
    has to be escaped.
    
    Parameters
    ----------
    string
        The markup text.
    
    args
        Variables to insert positional.
    
    kwargs
        Variables to insert by keyword.
    
    style
        Mapping of keys and the style to use.
        You may want to use
        :function:`utils.retrieve_ansi(locals())`.
    
    Returns
    -------
    Styled text.
    """
    text = XMLEscapeFormatter().format(string, *args, **kwargs)
    
    root = ET.fromstring(f"<root>{text}</root>")
    text = root.text or ""
    text += "".join(style_element(root, style = style))
    
    return html.unescape(text)
