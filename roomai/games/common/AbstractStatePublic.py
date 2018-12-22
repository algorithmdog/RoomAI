#!/bin/python
#coding=utf8

import roomai.games.common

logger = roomai.get_logger()

######################################################################### Basic Concepts #####################################################
class AbstractStatePublic(object):
    '''
    The abstract class of the public state. The information in the public state is public to every player.\n
    The attributes with param prefix is the parameters set by the init function of enviroment.
    '''
    def __init__(self):
        self.__turn__                        = None
        ## parameters
        self.__param_num_normal_players__    = 2
        self.__is_terminal__                 = False
        self.__scores__                      = None


    def __get_turn__(self): return self.__turn__
    turn = property(__get_turn__, doc = "The players[turn] is expected to take an action.")

    def __get_param_num_normal_players__(self):
        return self.__param_num_normal_players__
    param_num_normal_players = property(__get_param_num_normal_players__, doc="The number of normal players in the game.")

    def __get_is_terminal__(self):   return  self.__is_terminal__
    is_terminal = property(__get_is_terminal__,doc = "is_terminal = True means the game is over. At this time, scores is not None, scores = [float0,float1,...] for player0, player1,... For example, scores = [-1,2,-1].\n"
                                                     "is_terminal = False, the scores is None.")

    def __get_scores__(self):
        if self.__scores__ is None:
            return None
        return tuple(self.__scores__)
    scores = property(__get_scores__, doc = "is_terminal = True means the game is over. At this time, scores is not None, scores = [float0,float1,...] for player0, player1,... For example, scores = [-1,3,-2].\n"
                                            "is_terminal = False, the scores is None.")





    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = AbstractStatePublic()

        newinstance.__turn__           = self.__turn__
        newinstance.__is_terminal__    = self.is_terminal

        newinstance.__param_num_normal_players__ = self.__param_num_normal_players__

        if self.scores is None:
            newinstance.__scores__ = None
        else:
            newinstance.__scores__ = [score for score in self.scores]
        return newinstance