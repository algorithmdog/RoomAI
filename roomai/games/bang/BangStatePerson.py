#!/bin/python
from roomai.games.common import AbstractStatePerson

class BangStatePerson(AbstractStatePerson):
    def __init__(self):
        self.__hand_cards__ = []
        self.__role__       = None
