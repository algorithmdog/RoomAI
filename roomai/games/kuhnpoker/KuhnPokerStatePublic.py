#!/bin/python
import roomai.games.common

class KuhnPokerStatePublic(roomai.games.common.AbstractStatePublic):
    '''
    The public state class of the KuhnPoker game
    '''
    def __init__(self):
        super(KuhnPokerStatePublic, self).__init__()
        self.__param_start_turn__           = 0


    def ___get_start_turn__(self):    return self.__param_start_turn__
    first = property(___get_start_turn__, doc="players[param_start_turn] is first to take an action")


    def __deepcopy__(self, memodict={}):
        newinstance = KuhnPokerStatePublic()
        newinstance = super(KuhnPokerStatePublic, self).__deepcopy__(newinstance=newinstance)
        newinstance.__param_start_turn__ = self.__param_start_turn__
        return newinstance

