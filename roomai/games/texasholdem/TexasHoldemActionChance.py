#!/bin/python
#coding:utf-8
import roomai.games.common
from roomai.games.texasholdem.TexasHoldemUtil import AllPokerCardsDict
from roomai.games.texasholdem.TexasHoldemUtil import PokerCard

class TexasHoldemActionChance(roomai.games.common.AbstractActionChance):
    '''
    The TexasHoldemActionChance is the action used by the chance action\n
    The option is one of "Fold","Check","Call","Raise","AllIn", and the price is the chips used by this action.\n
    When the option is Fold or Check, the price must be 0.\n
    The TexasHoldemAction has a key "%s_%d"%(option, price) as its identification. Examples of usages:\n
    >> import roomai.TexasHoldem\n
    >> a = roomai.TexasHoldem.TexasHoldemAction.lookup("Fold_0")\n
    >> ## We strongly recommend you to get a TexasHoldemAction using the lookup function\n
    >> a.option \n
    "Fold"\n
    >> a.price\n
    0\n
    '''
    
    

    def __init__(self, key):
        super(TexasHoldemActionChance, self).__init__(key)
        self.__key__  = key
        self.__card__ = PokerCard.lookup(key)
        self.__is_public__ = False

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc = "The key of this action. For example, the key is \"A_Heart\".")

    def __get_card__(self):
        return self.__card__
    card = property(__get_card__, doc = "The normalcard of this action. For example, the normalcard is roomai.common.Card.lookup(\"A_Heart\")")


    @classmethod
    def lookup(cls, key):
        '''
        lookup an action with this specified key
        
        :param key: The specified key
        :return: The action
        '''
        logger = roomai.get_logger()
        if key not in AllTexasActionChances:
            logger.fatal("%s is not a valid action chance key"%(key))
            raise ValueError("%s is not a valid action chance key"%(key))

        return AllTexasActionChances[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        return TexasHoldemActionChance.lookup(self.key)

AllTexasActionChances = dict()
for pokercard_key in AllPokerCardsDict:
    AllTexasActionChances[pokercard_key] = TexasHoldemActionChance(pokercard_key)


