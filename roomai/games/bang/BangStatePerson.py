#!/bin/python
from roomai.games.common import AbstractStatePerson

class BangStatePerson(AbstractStatePerson):
    def __init__(self):
        self.__hand_cards__ = []
        self.__role__       = None

    def __get_hand_cards__(self):   return tuple(self.__hand_cards____)
    hand_cards = property(__get_hand_cards__, doc="The player info in public")

    def __get_role__(self):   return self.__role__
    role = property(__get_role__, doc="the role of the corresponding player")
