#!/bin/python

from roomai.games.common import AbstractStatePrivate

class BangStatePrivate(AbstractStatePrivate):
    def __init__(self):
        self.__deck__         = []
        self.__shuffle_deck__ = []
        self.__deal_cards__   = []


    def __get_deck__(self):  return tuple(self.__deck__)
    deck = property(__get_deck__, doc="the deck of this game")

    def __get_deal_cards__(self):  return tuple(self.__deal_cards__)
    deal_cards = property(__get_deal_cards__, doc="the dealed cards of this game")

    def __get_shuffle_deck__(self): return tuple(self.__shuffle_deck__)
    shuffle_deck = property(__get_shuffle_deck__, doc="the shuffle deck is as a tmp deck and used for shuffle")
