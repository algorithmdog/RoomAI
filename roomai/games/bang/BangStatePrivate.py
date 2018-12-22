#!/bin/python

from roomai.games.common import AbstractStatePrivate

class BangStatePrivate(AbstractStatePrivate):
    def __init__(self):
        self.__deck__        = []

    def __get_deck__(self):  return tuple(self.__deck__)
    deck = property(__get_deck__, doc="the card deck of this game")

