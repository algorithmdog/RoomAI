#!/bin/python

class PlaceholderAction:
    '''
    The placeholderaction . 
    '''

    def __init__(self, key):
        if not isinstance(key,str):
            raise TypeError("The key for Action is an str, not %s"%(type(str)))
        self.__key__        = key

    def __get_key__(self):
        return self.__key__


    key = property(__get_key__, doc="The key of the action. Every action in RoomAI has a key as its identification."
                                    " We strongly recommend you to use the lookup function to get an action with the specified key")

    @classmethod
    def lookup(self, key):
        return placeholderaction

    def __deepcopy__(self, memodict={}, newinstance=None):
        return placeholderaction

placeholderaction = PlaceholderAction("placeholder")

class ActionRecord(object):
    def __init__(self, playerid, action):
        self.__playerid__ = playerid
        if action.is_public == True:
            self.__action__   = action
        else:
            self.__action__   = placeholderaction

    def __get_playerid__(self):
        return self.__playerid__
    playerid = property(__get_playerid__)

    def __get_action__(self):
        return self.__action__
    action = property(__get_action__)
