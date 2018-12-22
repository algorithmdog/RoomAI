#!/bin/python

from roomai.games.common import AbstractStatePrivate

class BangStatePrivate(AbstractStatePrivate):
    def __init__(self):
        self.__library__        = []

    def __get_library__(self):  return tuple(self.__library__)
    library = property(__get_library__, doc="the library of this game")

