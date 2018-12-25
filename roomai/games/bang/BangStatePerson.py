#!/bin/python
from roomai.games.common import AbstractStatePerson

class BangStatePerson(AbstractStatePerson):
    def __init__(self):
        self.__hand_cards__ = []
        self.__role__       = None
        self.__hp__         = -1

    def __get_hand_cards__(self):   return tuple(self.__hand_cards____)
    hand_cards = property(__get_hand_cards__, doc="The player info in public")

    def __get_role__(self):   return self.__role__
    role = property(__get_role__, doc="the role of the corresponding player")

    def __get_hp__(self):   return self.__hp__
    hp = property(__get_hp__, doc = "the hp of the corresponding player")