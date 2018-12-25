#!/bin/python
#coding:utf-8
import re

import roomai.games.common


class TexasHoldemAction(roomai.games.common.AbstractAction):
    '''
    The TexasHoldemAction. The action consists of two parts, namely option and price.\n
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
    
    
    # 弃牌
    Fold        = "Fold"
    # 过牌
    Check       = "Check"
    # 更注
    Call        = "Call"
    # 加注
    Raise       = "Raise"
    # all in
    AllIn       = "Allin"
    def __init__(self, key):
        if re.match("^Allin_[1-9]\d*|Raise_[1-9]\d*|Call_[1-9]\d*|Fold_0|Check_0$", key) is None:
            raise ValueError("%s is invalid key for TexasHoldemAction. The TexasHoldemAction has a key option_price, Fold_0 for example. When the option is Fold or Check, the price must be 0. The check regrex is ^Allin_[1-9]\d*|Raise_[1-9]\d*|Call_[1-9]\d*|Fold_0|Check_0$"%(key))


        opt_price = key.strip().split("_")
        self.__option__ = opt_price[0]
        self.__price__  = int(opt_price[1])
        self.__key__    = "%s_%d"%(self.option, self.price)
        self.__is_public__ = True
        if self.__option__ == self.Fold or self.__option__ == self.Check:
            if self.price > 0:
                raise ValueError("%s is invalid key for TexasHoldemAction. The %s option only matches the zero price"%(self.__key__, self.__option__))


    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc = "The key of this action. For example, the key is \"Fold_0\".")

    def __get_option__(self):
        return self.__option__
    option = property(__get_option__, doc = "The option of this action. The option must be one of \"Fold\",\"Check\",\"Call\",\"Raise\",\"AllIn\".")
    
    
    def __get_price__(self):
        return self.__price__
    price = property(__get_price__, doc = "The price of this action. For example, the price is 0")

    @classmethod
    def lookup(cls, key):
        '''
        lookup an action with this specified key
        
        :param key: The specified key
        :return: The action
        '''
        if key not in AllTexasActions:
            AllTexasActions[key] = TexasHoldemAction(key)
        return AllTexasActions[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        if self.key not in AllTexasActions:
            AllTexasActions[self.key] = TexasHoldemAction(self.key)
        return AllTexasActions[self.key]

AllTexasActions = dict()
