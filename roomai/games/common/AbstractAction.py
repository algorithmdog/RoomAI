#!/bin/python
# coding=utf8

import roomai.games.common

logger = roomai.get_logger()


class AbstractAction(object):
    '''
    The abstract class of an action. 
    '''

    def __init__(self, key):
        if not isinstance(key,str):
            raise TypeError("The key for Action is an str, not %s"%(type(str)))

        self.__key__        = key
        self.__is_public__  = True

    def __get_key__(self):
        return self.__key__



    key = property(__get_key__, doc="The key of the action. Every action in RoomAI has a key as its identification."
                                    " We strongly recommend you to use the lookup function to get an action with the specified key")

    def __get_is_public__(self):    return self.__is_public__
    is_public = property(__get_is_public__, doc="The actions in RoomAI can be categorized into two classes: the public action and the private action."
                                                "The private action will be replaced by PlaceholderAction in the playerid_action_history")

    @classmethod
    def lookup(self, key):
        '''
        Get an action with the specified key. \n
        We strongly recommend you to use the lookup function to get an action with the specified key, rather than use the constructor function.\n

        :param key: the specified key
        :return:  the action with the specified key
        '''
        raise NotImplementedError("Not implemented")



    def __deepcopy__(self, memodict={}, newinstance=None):
        if newinstance is None:
            newinstance = AbstractAction()
        newinstance.__key__ = self.__key__
        return newinstance