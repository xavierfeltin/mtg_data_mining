# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#

import sys

class Card:

    JSON_WHITE = 'W'
    JSON_BLUE = 'U'
    JSON_BLACK = 'B'
    JSON_RED = 'R'
    JSON_GREEN = 'G'

    STRING_WHITE = 'white'
    STRING_BLUE = 'blue'
    STRING_BLACK = 'black'
    STRING_RED = 'red'
    STRING_GREEN = 'green'
    STRING_NO_COLOR = 'no_color'

    CODE_WHITE = 1
    CODE_BLUE = 2
    CODE_BLACK = 4
    CODE_RED = 8
    CODE_GREEN = 16
    CODE_NO_COLOR = 32

    def __init__(self, multiverseid, name, mana_cost, types, colors, full_text, description):
        self.multiverseid = multiverseid
        self.name = name
        self.mana_cost = mana_cost
        self.types = types
        self.colors = colors
        self.full_text = full_text
        self.description = description
        self.code_color = self.get_color_code()

    def get_color_code(self):
        value = 0
        for color in self.colors :
            color = color.upper()
            if color == Card.JSON_BLACK:
                value = value | Card.CODE_BLACK
            elif color == Card.JSON_BLUE:
                value = value | Card.CODE_BLUE
            elif color == Card.JSON_WHITE:
                value = value | Card.CODE_WHITE
            elif color == Card.JSON_RED:
                value = value | Card.CODE_RED
            elif color == Card.JSON_GREEN:
                value = value | Card.CODE_GREEN
            else:
                value = value | Card.CODE_NO_COLOR
        return value

    def get_colors_names(self):
        if len(self.colors) == 0:
            return [Card.STRING_NO_COLOR]
        else:
            colors = []
            for abbr in self.colors:
                if abbr == Card.JSON_BLACK: colors.append(Card.STRING_BLACK)
                if abbr == Card.JSON_BLUE: colors.append(Card.STRING_BLUE)
                if abbr == Card.JSON_GREEN: colors.append(Card.STRING_GREEN)
                if abbr == Card.JSON_RED: colors.append(Card.STRING_RED)
                if abbr == Card.JSON_WHITE: colors.append(Card.STRING_WHITE)
            return colors

    def is_basic_land(self):
        return ('Land' in self.types and self.description == '')