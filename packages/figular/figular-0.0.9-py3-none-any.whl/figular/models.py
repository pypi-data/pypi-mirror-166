# SPDX-FileCopyrightText: 2021-2 Galagic Limited, et. al. <https://galagic.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# figular generates visualisations from flexible, reusable parts
#
# For full copyright information see the AUTHORS file at the top-level
# directory of this distribution or at
# [AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from enum import Enum
from pydantic import BaseModel, constr, conint, confloat
from typing import Optional
import re
import string


class ColorEnum(str, Enum):
    Black = 'Black'
    Cyan = 'Cyan'
    Magenta = 'Magenta'
    Yellow = 'Yellow'
    black = 'black'
    blue = 'blue'
    brown = 'brown'
    chartreuse = 'chartreuse'
    cyan = 'cyan'
    darkblue = 'darkblue'
    darkbrown = 'darkbrown'
    darkcyan = 'darkcyan'
    darkgray = 'darkgray'
    darkgreen = 'darkgreen'
    darkgrey = 'darkgrey'
    darkmagenta = 'darkmagenta'
    darkolive = 'darkolive'
    darkred = 'darkred'
    deepblue = 'deepblue'
    deepcyan = 'deepcyan'
    deepgray = 'deepgray'
    deepgreen = 'deepgreen'
    deepgrey = 'deepgrey'
    deepmagenta = 'deepmagenta'
    deepred = 'deepred'
    deepyellow = 'deepyellow'
    fuchsia = 'fuchsia'
    gray = 'gray'
    green = 'green'
    grey = 'grey'
    heavyblue = 'heavyblue'
    heavycyan = 'heavycyan'
    heavygray = 'heavygray'
    heavygreen = 'heavygreen'
    heavygrey = 'heavygrey'
    heavymagenta = 'heavymagenta'
    heavyred = 'heavyred'
    lightblue = 'lightblue'
    lightcyan = 'lightcyan'
    lightgray = 'lightgray'
    lightgreen = 'lightgreen'
    lightgrey = 'lightgrey'
    lightmagenta = 'lightmagenta'
    lightolive = 'lightolive'
    lightred = 'lightred'
    lightyellow = 'lightyellow'
    magenta = 'magenta'
    mediumblue = 'mediumblue'
    mediumcyan = 'mediumcyan'
    mediumgray = 'mediumgray'
    mediumgreen = 'mediumgreen'
    mediumgrey = 'mediumgrey'
    mediummagenta = 'mediummagenta'
    mediumred = 'mediumred'
    mediumyellow = 'mediumyellow'
    olive = 'olive'
    orange = 'orange'
    paleblue = 'paleblue'
    palecyan = 'palecyan'
    palegray = 'palegray'
    palegreen = 'palegreen'
    palegrey = 'palegrey'
    palemagenta = 'palemagenta'
    palered = 'palered'
    paleyellow = 'paleyellow'
    pink = 'pink'
    purple = 'purple'
    red = 'red'
    royalblue = 'royalblue'
    salmon = 'salmon'
    springgreen = 'springgreen'
    white = 'white'
    yellow = 'yellow'


class BorderStyleEnum(str, Enum):
    solid = 'solid'
    dotted = 'dotted'
    dashed = 'dashed'
    longdashed = 'longdashed'
    dashdotted = 'dashdotted'
    longdashdotted = 'longdashdotted'


class FontEnum(str, Enum):
    avantgarde = 'Avant Garde'
    bookman = 'Bookman'
    computermodern_roman = 'Computer Modern Roman'
    computermodern_sansserif = 'Computer Modern Sans'
    computermodern_teletype = 'Computer Modern Teletype'
    courier = 'Courier'
    dejavu_sansserif = 'DejaVu Sans'
    helvetica = 'Helvetica'
    newcenturyschoolbook = 'New Century Schoolbook'
    palatino = 'Palatino'
    symbol = 'Symbol'
    timesroman = 'Times New Roman'
    zapfchancery = 'Zapf Chancery'
    zapfdingbats = 'Zapf Dingbats'


class Circle(BaseModel):
    background_color: Optional[ColorEnum]
    border_color: Optional[ColorEnum]
    border_width: Optional[confloat(ge=0, le=100)]
    border_style: Optional[BorderStyleEnum]
    color: Optional[ColorEnum]
    font_family: Optional[FontEnum]
    font_size: Optional[confloat(ge=0, le=300)]

    def getasy(self):
        cleanArgs = []
        if self.background_color:
            cleanArgs.append(
                f"fillcolor={self.background_color}")
        if self.border_color:
            cleanArgs.append(
                f"strokecolor={self.border_color}")
        if self.border_width:
            cleanArgs.append(
                f"strokewidth={self.border_width}")
        if self.border_style:
            cleanArgs.append(
                f"dashes={self.border_style}")
        if self.color:
            cleanArgs.append(
                f"textcolor={self.color}")
        if self.font_family:
            cleanArgs.append(
                f"text=font.{self.font_family.name}")
        if self.font_size:
            cleanArgs.append(
                f"textsize={self.font_size}")
        if cleanArgs:
            return f"setupstyleforcircles(style({','.join(cleanArgs)}))"
        return ""


class FigureCircleStyle(BaseModel):
    rotation: Optional[conint(ge=0, le=360)]
    middle: Optional[bool]

    def getasy(self):
        cleanArgs = []
        if self.rotation:
            cleanArgs.append(
                f"degreeStart={self.rotation}")
        if self.middle:
            cleanArgs.append(
             "middle="
             f"{str(self.middle).lower()}")
        return f"registercirclestyle({','.join(cleanArgs)})"


class Style(BaseModel):
    figure_concept_circle: Optional[FigureCircleStyle]
    circle: Optional[Circle]


class Message(BaseModel):
    """ Inputs for the concept/circle figure """

    # [Flake8 raises "syntax error in forward annotation" on regex
    # constraints](https://github.com/samuelcolvin/pydantic/issues/2872)
    data: constr(regex=('^[' +                                 # noqa: F722
                        re.escape(string.printable) + ']+$'),  # noqa: F722
                 min_length=1,
                 # Pydantic v2 will allow us to relax this limit depending
                 # on context (cmdline v api)
                 # https://pydantic-docs.helpmanual.io/blog/pydantic-v2/#validation-context
                 max_length=5000)
    style: Optional[Style]

    def getasy(self):
        cleanArgs = []
        if self.style:
            if self.style.figure_concept_circle:
                cleanArgs.append(self.style.figure_concept_circle.getasy())
            if self.style.circle:
                cleanArgs.append(self.style.circle.getasy())
        return f"{';'.join(cleanArgs)};"
