#!/bin/python
import roomai.games.common
import copy


class KuhnPokerActionChance(roomai.games.common.AbstractActionChance):
    '''
    The KuhnPoker action used by the chance player. Example of usages:\n
    >> import roomai.kuhnpoker\n
    >> action = roomai.kuhnpoker.KuhnPokerChanceAction.lookup("0,1")\n
    >> action.key \n
    "0,1"\n
    >> action.number_for_player0\n
    0\n
    >> action.number_for_player1\n
    1\n
    '''

    def __init__(self, key):
        super(KuhnPokerActionChance, self).__init__(key)
        self.__key__ = key
        n1_n2        = key.split(",")
        self.__number_for_player0 = int(n1_n2[0])
        self.__number_for_player1 = int(n1_n2[1])
        self.__is_public__ = False

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the KuhnPokerChance action, for example, \"0,1\"")

    def __get_number_for_player0__(self):
        return self.__number_for_player0
    number_for_player0 = property(__get_number_for_player0__, doc = "The number of the players[0]")

    def __get_number_for_player1__(self):
        return self.__number_for_player1
    number_for_player1 = property(__get_number_for_player1__, doc = "The number of the players[1]")

    @classmethod
    def lookup(cls, key):
        return AllKuhnChanceActions[key]

    def mask(self):
        AllKuhnChanceActions["-1,-1"]


    def __deepcopy__(self, memodict={}):
        return KuhnPokerActionChance.lookup(self.key)

AllKuhnChanceActions = {"0,1": KuhnPokerActionChance("0,1"), \
                        "1,0": KuhnPokerActionChance("1,0"),\
                        "0,2": KuhnPokerActionChance("0,2"), \
                        "2,0": KuhnPokerActionChance("2,0"), \
                        "1,2": KuhnPokerActionChance("1,2"), \
                        "2,1": KuhnPokerActionChance("2,1")}



