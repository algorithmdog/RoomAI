#!/bin/python

from roomai.games.common import AbstractActionChance

from roomai.games.bang import PlayingCard
from roomai.games.bang import CharacterCard
from roomai.games.bang import RoleCard
from roomai.games.bang import AllPlayingCardsDict
from roomai.games.bang import AllCharacterCardsDict
from roomai.games.bang import AllRoleCardsDict

import roomai

class BangActionChanceType:
    rolecard = "rolecard"
    charactercard = "charactercard"
    playingcard = "playingcard"


class BangActionChance(AbstractActionChance):
    def __init__(self, key):
        logger = roomai.get_logger()
        self.__is_public__ = False
        if key in AllPlayingCardsDict:
            self.__type__ = BangActionChanceType.playingcard
            self.__card__ = PlayingCard.lookup(key)
            self.__key__  = key
        elif key in AllCharacterCardsDict:
            self.__type__ = BangActionChanceType.charactercard
            self.__card__ = CharacterCard.lookup(key)
            self.__key__  = key
        elif key in AllRoleCardsDict:
            self.__type__ = BangActionChanceType.rolecard
            self.__card__ = RoleCard.lookup(key)
            self.__key__  = key
        else:
            logger.fatal("In the constructor BangActionChance(card), the parameter card must be NormalCard, CharacterCard or RoleCard")
            raise TypeError("In the constructor BangActionChance(card), the parameter card must be NormalCard, CharacterCard or RoleCard")

    def __get_type__(self): return self.__type__
    type = property(__get_type__, doc = "the type of BangActionChance, e.g., type=%s, type=%s or type=%s"%(BangActionChanceType.rolecard, BangActionChanceType.playingcard, BangActionChanceType.charactercard))

    def __get_card__(self): return  self.__card__
    card = property(__get_card__, doc = "the card of BangActionChance")

    def __get_key__(self):  return self.__card__.key
    key = property(__get_key__, doc = "the key of the BangActionChance. In fact, the key is the key of the card in this BangActionChance")

    @classmethod
    def lookup(self, key):
        logger = roomai.get_logger()
        if key is None or not isinstance(key,str):
            logger.fatal("In the constructor BangActionChance.lookup(key), the key must be a str")
            raise TypeError("In the constructor BangActionChance.lookup(key), the key must be a str")
        if key not in AllBangActionChancesDict:
            logger.fatal("In the constructor BangActionChance.lookup(key), the key must be the key of CharacterCard, RoleCard or PlayingCard")
            raise ValueError("In the constructor BangActionChance.lookup(key), the key must be the key of CharacterCard, RoleCard or PlayingCard")
        return AllBangActionChancesDict[key]

    def __deepcopy__(self, memodict={}):
        return AllBangActionChancesDict[self.__key__]


AllBangActionChancesDict = dict()
for key, value in AllPlayingCardsDict.items():
    AllBangActionChancesDict[key] = value
for key, value in AllCharacterCardsDict.items():
    AllBangActionChancesDict[key] = value
for key, value in AllRoleCardsDict.items():
    AllBangActionChancesDict[key] = value
