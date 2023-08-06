from os import environ, system
from platform import uname
from enum import Enum
from typing import Union

class colours(Enum):
    """Class containing all available colours to use in colour-splash"""
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    magenta = 5
    cyan = 6
    white = 7
    none = 9

class styles(Enum):
    """Class containing all available styles to use in colour-splash"""
    none = 0
    bright = 1
    dim = 2
    italic = 3
    underline = 4
    slow_blink = 5
    fast_blink = 6
    invert = 7
    hide = 8
    strikethrough = 9
    double_underline = 21
    overline = 53

class rgb:
    """Defines a specific RGB colour value"""
    red = 0
    green = 0
    blue = 0
    def __init__(self, red:int, green:int, blue:int):
        self.red = red
        self.green = green
        self.blue = blue

class settings:
    """Class containing all settings to configure colour-splash behaviours"""
    force_colours = False
    no_colours = False

class __config:
    """Class containing information about the ANSI colour codes"""
    escape_start = "\033[0;"
    escape_end = "m"

    colour_prefix = {
        "foreground": 3,
        "background": 4
    }

    colour_suffix = {
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
        "none": 9,
    }

    style_prefix = {
        "none": 0,
        "bright": 1,
        "dim": 2,
        "italic": 3,
        "underline": 4,
        "slow blink": 5, 
        "fast blink": 6,
        "invert": 7,
        "hide": 8,
        "strikethrough": 9,
        "double underline": 21,
        "overline": 53,
    }

colour_list = []
supports_colour = "TERM" in environ.keys() or "WT_SESSION" in environ.keys()
system("")

if "PROMPT" not in environ.keys() and uname().system == "Windows" and not supports_colour:
    supports_colour = True

def colour(text:str, foreground:Union[str,colours,rgb] = colours.none, background:Union[str,colours,rgb] = colours.none):
    """Returns text formatted with a background and foreground colour"""
    if type(foreground) == str:
        if foreground not in __config.colour_suffix:
            raise ValueError(f"\"{foreground}\" is not a valid colour")
        foreground_value = f"3{__config.colour_suffix[foreground]}"
    elif type(foreground) == colours:
        if foreground not in colours:
            raise ValueError(f"\"{foreground.name}\" is not a valid colour name")
        foreground_value = f"3{foreground.value}"
    elif type(foreground) == rgb:
        if not(0 <= foreground.red <= 255 and 0 <= foreground.green <= 255 and 0 <= foreground.blue <= 255):
            raise ValueError(f"\"({foreground.red},{foreground.green},{foreground.blue}) is not a valid rgb colour code")
        foreground_value = f"38;2;{foreground.red};{foreground.green};{foreground.blue}"

    if type(background) == str:
        if background not in __config.colour_suffix:
            raise ValueError(f"\"{background}\" is not a valid colour")
        background_value = f"4{__config.colour_suffix[background]}"
    elif type(background) == colours:
        if background not in colours:
            raise ValueError(f"\"{background.name}\" is not a valid colour name")
        background_value = f"4{background.value}"
    elif type(background) == rgb:
        if not(0 <= background.red <= 255 and 0 <= background.green <= 255 and 0 <= background.blue <= 255):
            raise ValueError(f"\"({background.red},{background.green},{background.blue}) is not a valid rgb colour code")
        background_value = f"48;2;{background.red};{background.green};{background.blue}"
        
    prefix = f"{__config.escape_start}{foreground_value};{background_value}{__config.escape_end}"
    suffix = f"{__config.escape_start}39;49{__config.escape_end}"

    return f"{prefix}{text}{suffix}"

def style(text:str, decoration:Union[styles, str] = styles.none):
    """Returns text formatted with a style"""
    if not (supports_colour or settings.force_colours) or settings.no_colours:
        return text

    style_num = __config.style_prefix[decoration] if type(decoration) == str else style.value

    if type(decoration) == str:
        if decoration not in __config.style_prefix:
            raise ValueError(f"\"{decoration}\" is not a valid colour")
    else:
        if decoration not in styles:
            raise ValueError(f"\"{decoration.name}\" is not a valid colour")

    prefix = f"{__config.escape_start}{style_num}{__config.escape_end}"
    suffix = suffix = f"{__config.escape_start}0{__config.escape_end}"
    return f"{prefix}{text}{suffix}"

def colour_start(foreground:Union[str,colours,rgb] = colours.none, background:Union[str,colours,rgb] = colours.none):
    """Returns a starter for text formatted with a background and foreground colour. Any text following will be in that colour"""
    if not (supports_colour or settings.force_colours) or settings.no_colours:
        return

    colour_list.append([foreground, background, "none"])
    return colour("~", foreground, background).split("~")[0]

def colour_end():
    """Stops the current colour from being used. Any text following will be in the previous colour/style"""
    if not (supports_colour or settings.force_colours) or settings.no_colours:
        return

    global colour_list
    if len(colour_list) == 0:
        return
    
    if len(colour_list) == 1:
        colour_list = colour_list[0:-1]
        return colour("", "none", "none") + style("", "none")
    
    previous_colour = colour_list[-2]
    colour_list = colour_list[0:-1]
    if previous_colour[0] == "none" and previous_colour[1] == "none" and previous_colour[2] != ["none"]:
        return f"{__config.escape_start}{__config.style_prefix[previous_colour[2]]}{__config.escape_end}"

    return colour("~", previous_colour[0], previous_colour[1]).split("~")[0]

def style_start(decoration:Union[str,styles] = "none"):
    """Returns a starter for text formatted with a style. Any text following will be in that style"""
    if not (supports_colour or settings.force_colours) or settings.no_colours:
        return

    colour_list.append(["none", "none", decoration])
    return style("~", decoration).split("~")[0]

def style_end():
    """Stops the current style from being used. Any text following will be in the previous colour/style"""
    if not (supports_colour or settings.force_colours) or settings.no_colours:
        return
    return colour_end()

def help():
    """Outputs all available colours using keywords"""
    print("Foreground Colours")
    for _colour in __config.colour_suffix:
        print("  \u21B3", f"\"{_colour}\"", "foreground: ", colour(_colour, foreground = _colour))

    print("Background Colours")
    for _colour in __config.colour_suffix:
        print("  \u21B3", f"\"{_colour}\"", "background: ", colour(_colour, background = _colour))

    print("Styles")
    for _style in __config.style_prefix:
        print("  \u21B3", f"\"{_style}\"", "style: ", style(_style, _style))