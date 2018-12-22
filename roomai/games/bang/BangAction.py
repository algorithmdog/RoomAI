#!/bin/python
#coding:utf-8

from roomai.games.common import AbstractAction
from roomai.games.bang import AllPlayingCardsDict
from roomai.games.bang import PlayingCardNames

class BangActionType:
    card = "card"
    skill = "skill"

class BangAction(AbstractAction):
    def __init__(self, key):

        self.__card__ = None
        self.__skill__ = None
        self.__source__ = None
        self.__first_target__ = None
        self.__second_target__ = None
        self.__key__ = None

        keys = key.split("_")
        if keys[0] in AllPlayingCardsDict:
            self.__type__ = BangActionType.card
            self.__card__ = AllPlayingCardsDict[keys[0]]
        else:
            self.__type__ = BangActionType.skill
            self.__skill__ =




    @classmethod
    def lookup(self, key):
        raise NotImplementedError

    def __get_card__(self): return self.__card__
    card = property(__get_card__, doc="the card used in this action")

    def __get_source__(self): return self.__source__
    source = property(__get_source__, doc="the id of the player, who issues this action")

    def __get_first_target__(self): return self.__first_target__
    first_target = property(__get_first_target__,doc = "the first target of this action")

    def __get_second_target__(self): return self.__second_target__
    second_target = property(__get_second_target__, doc = "the second target of this action")



AllBangActionsDict = dict()
for playingcard in AllPlayingCardsDict:
    if playingcard.name == PlayingCardNames.Duello:

        AllPlayingCardsDict[playingcard.key] = action

    elif card.name == PlayingCardNames.Carabine:
        pass
    elif card.name == PlayingCardNames.Bang:
        pass
    elif card.name == PlayingCardNames.Emporia:
        pass
    elif card.name == PlayingCardNames.Volcanic:
        pass
    elif card.name == PlayingCardNames.Schofield:
        pass
    elif card.name == PlayingCardNames.Remington:
        pass
    elif card.name == PlayingCardNames.Panic:
        pass
    elif card.name == PlayingCardNames.Dynamite:
        pass
    elif card.name == PlayingCardNames.WellsFargo:
        pass
    elif card.name == PlayingCardNames.Prigione:
        pass
    elif card.name == PlayingCardNames.Saloon:
        pass
    elif card.name == PlayingCardNames.Beer:
        pass
    elif card.name == PlayingCardNames.Catling:
        pass
    elif card.name == PlayingCardNames.CatBalou:
        pass
    elif card.name == PlayingCardNames.Miss:
        pass
    elif card.name == PlayingCardNames.StageCoach:
        pass
    elif card.name == PlayingCardNames.Barrel:
        pass
    elif card.name == PlayingCardNames.Mustang:
        pass
    elif card.name == PlayingCardNames.Indian:
        pass
    elif card.name == PlayingCardNames.Winchester:
        pass
    elif card.name == PlayingCardNames.Appaloosa:
        pass