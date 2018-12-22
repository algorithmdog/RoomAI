#!/bin/bash
import roomai

class RoleCardNames:
    sheriff        = "sheriff"
    deputy_sheriff = "deputy_sheriff"
    outlaw         = "outlaw"
    renegade       = "renegade"

class RoleCard(object):

    def __init__(self, role):
        logger = roomai.get_logger()
        if isinstance(role, str):
            logger.fatal("In the constructor RoleCard(rolecard), the rolecard must be a str.")
            raise TypeError("In the constructor RoleCard(rolecard), the rolecard must be a str.")
        if role not in [RoleCardNames.sheriff, RoleCardNames.deputy_sheriff, RoleCardNames.outlaw, RoleCardNames.renegade]:
            logger.fatal("In the constructor RoleCard(rolecard), the rolecard must be one of [%s,%s,%s,%s]"%(RoleCardNames.sheriff, RoleCardNames.deputy_sheriff, RoleCardNames.outlaw, RoleCardNames.renegade))
            raise TypeError("In the constructor RoleCard(rolecard), the rolecard must be one of [%s,%s,%s,%s]"%(RoleCardNames.sheriff, RoleCardNames.deputy_sheriff, RoleCardNames.outlaw, RoleCardNames.renegade))

        self.__name1__ = role

    def __get_name__(self):
        return self.__name1__
    name = property(__get_name__, doc="The name of the role card")

    def __get_key__(self):  return self.__role__
    key = property(__get_key__, doc = "The key of role card")

    @classmethod
    def lookup(cls, key):
        logger = roomai.get_logger()
        if key not in AllRoleCardsDict:
            logger.fatal("%s is not valid rolecard key"%(key))
            raise TypeError("%s is not valid rolecard key"%(key))
        return AllRoleCardsDict[key]

    def __deepcopy__(self, memodict={}):
        return AllRoleCardsDict[self.key]

AllRoleCardsDict = dict()
AllRoleCardsDict[RoleCardNames.sheriff]        = RoleCard(RoleCardNames.sheriff)
AllRoleCardsDict[RoleCardNames.deputy_sheriff] = RoleCard(RoleCardNames.deputy_sheriff)
AllRoleCardsDict[RoleCardNames.outlaw]         = RoleCard(RoleCardNames.outlaw)
AllRoleCardsDict[RoleCardNames.renegade]       = RoleCard(RoleCardNames.renegade)