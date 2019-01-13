#!/bin/python

from roomai.games.common import AbstractStatePublic

class PublicPlayerInfo(object):
    def __init__(self):
        self.__num_hand_cards__  = 0
        self.__character_card__  = None
        self.__equipment_cards__ = []
        self.__is_alive__        = True

    def __get_num_hand_cards__(self):   return self.__num_hand_cards__
    num_hand_cards = property(__get_num_hand_cards__,doc="The number of hand cards")

    def __get_character_card__(self):   return self.__character_card__
    character_card = property(__get_character_card__, doc="The character card")

    def __get_equipment_cards__(self):  return tuple(self.__equipment_cards__)
    get_equipment_cards = property(__get_equipment_cards__, doc="The equipment cards")

    def __get_is_alive__(self):  return self.__is_alive__
    is_alive = property(__get_is_alive__, doc="Whether does the corresponding player live")

    def __deepcopy__(self, memodict={}):
        info = PublicPlayerInfo
        info.__num_hand_cards__ = self.num_hand_cards

        if self.__character_card__ is None:
            info.__character_card__ = None
        else:
            info.__character_card__ = self.__character_card__.__deepcopy__()

        info.__equipment_cards__ = [a.__deepcopy__() for a in self.__equipment_cards__]
        return info


class PhaseInfo(object):
    Draw        = "Draw"
    Play        = "Play"
    Discard     = "Discard"
    def __init__(self):
        self.__playid__ = -1
        self.__phase__  = self.ChancePlay

    def __get_playerid__(self): return self.__playid__
    playerid = property(__get_playerid__, doc="Now the game is in the players[playerid]'s turn")

    def __get_phase__(self):    return self.__phase__
    phase = property(__get_phase__, doc = "Now the game is in the players[playerid]'s turn's phase. The phases are ChancePlay, Draw, Play, Discard")


    def __deepcopy__(self, memodict={}):
        info = PhaseInfo()
        info.__playid__ = self.__playid__
        info.__phase__  = self.__phase__
        return info




class ResponseInfo(object):

    ToDead = "ToDead"
    UseIndian = "UseIndian"
    UseCatling = "UseCatling"
    Shuffle = "Shuffle"

    def __init__(self):
        self.__subject__  = -1
        self.__object__   = -1
        self.__reason__   = -1

    def __get_reason__(self): return self.__reason__
    reason = property(__get_reason__,
                      doc="Now the players[responseinfo.subject] is responsing to the players[responseinfo.object] since response.reason")

    def __get_subject__(self):    return self.__subject__
    subject = property(__get_subject__,
                       doc="Now the players[responseinfo.subject] is responsing to the players[responseinfo.object] since response.reason")

    def __get_object__(self):   return self.__object__
    object = property(__get_object__,
                      doc="Now the players[responseinfo.subject] is responsing to the players[responseinfo.object] since response.reason")



    def __deepcopy__(self, memodict={}):
        info = ResponseInfo()
        info.__subject__ = self.__subject__
        info.__object__ = self.__object__
        info.__reason__ = self.__reason__
        return info

class BangStatePublic(AbstractStatePublic):

    def __init__(self):
        self.__public_player_infos__   = []
        self.__phase_info__            = PhaseInfo()
        self.__response_infos_stack__  = []
        self.__sheriff_id__            = -1
        self.__discard_pile__          = []
        self.__emporia_pile__          = []


    def __get_public_player_infos__(self):   return tuple(self.__public_player_infos__)
    public_player_infos = property(__get_public_player_infos__, doc="The player info in public")

    def __get_phase_info__(self):   return self.__phase_info__
    phase_info = property(__get_phase_info__, doc="The phase info indicates in which phase is the game")

    def __get_response_infos_stack__(self):  return tuple(self.__response_infos_stack__)
    response_infos_stack = property(__get_response_infos_stack__, doc="The response info indicates who and whos action is the players[turn] response to")

    def __get_sheriff_id__(self):   return self.__sheriff_id__
    sheriff_id = property(__get_sheriff_id__, doc="The id of the sheriff")

    def __get_discard_pile__(self): return tuple(self.__discard_pile__)
    discard_pile = property(__get_discard_pile__, doc="The discard pile of this game")

