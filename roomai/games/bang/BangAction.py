#!/bin/python
#coding:utf-8

from roomai.games.common import AbstractAction
from roomai.games.bang import AllPlayingCardsDict
from roomai.games.bang import PlayingCardNames
from roomai.games.bang import CharacterCardNames
from roomai.games.bang import ADeckOfCards
import roomai

AllBangActionsDict = dict()


class BangActionType(AbstractAction):
    card  = "card"
    skill = "skill"
    other = "other"

class OtherActionNames:
    giveup = "giveup"
    emporiachoose = "emporiachoose"
    draw = "draw"

class BangAction(AbstractAction):
    '''
    BangAction is the action played by the normal players \n\n
    The action key looks like "cardkey_firsttarget1:firsttarget2(option)_secondtarget1:secondtarget2(option)" or "charactername_seencards1:seencard2(option)_choosecard1:choosecard1(option)" or "otheraction_othertarget(option)"
    
    '''
    def __init__(self, key):
        logger = roomai.get_logger()
        self.__type__            = BangActionType.card
        self.__key__             = None

        self.__skill__           = None
        self.__seen_cards__      = set()
        self.__choosen_cards__   = set()

        self.__card__            = None
        self.__card_targets__    = []

        self.__other__           = None
        self.__other_targets__   = []

        keys = key.split("_")
        if keys[0] in AllPlayingCardsDict:
            self.__card__ = AllPlayingCardsDict[keys[0]]
        else:
            logger.info("%s is invalid action key, since the cardkey %s is invalid"%(key, keys[0]))

    @classmethod
    def lookup(self, key):
       return AllBangActionsDict[key]


    def __deepcopy__(self, memodict={}):
        a = BangAction()
        a.__type__  = self.__type__
        a.__key__   = self.__key__

        # about skill
        a.__skill__          = self.__skill__
        a.__seen_cards__     = set(list(self.__seen_cards__))
        a.__choosen_cards__  = set(list(self.__choosen_cards__))

        # about card
        a.__card__             = self.__card__
        a.__card_targets__     = list(tuple(self.__first_target__))

        # about other
        a.__other__             = self.__other__
        a.__other_targets__      = list(tuple(self.__othertargets__))

        return a

    def __get_type__(self): return self.__type__
    type = property(__get_type__, doc="the type of the bang action is %s or %s"%(BangActionType.card, BangActionType.skill))

    ## about skill
    def __get_skill__(self):    return self.__skill__
    skill = property(__get_skill__, doc="the skill used in this %s action"%(BangActionType.skill))

    def __get_seen_cards__(self):    return frozenset(self.__seen_cards__)
    seen_cards = property(__get_seen_cards__, doc = "the seen cards in this %s action. The seen card set may be empty"%(BangActionType.skill))

    def __get_choosen_cards__(self):  return frozenset(self.__choosencards__)
    choosen_cards = property(__get_choosen_cards__, doc="the choosen cards in this %s action. The choosen card set may be empty"%(BangActionType.skill))

    ## about card
    def __get_card__(self): return self.__card__
    card = property(__get_card__, doc="the card used in this %s action"%(BangActionType.card))

    def __get_card_targets__(self): return tuple(self.__card_targets__)
    card_targets = property(__get_card_targets__,doc = "the targets of this %s action. Generally, the number of the targets is 1."%(BangActionType.card))


    ## about other
    def __get_other__(self): return self.__other__
    other = property(__get_other__, doc="the other'key used in this %s action"%(BangActionType.other))

    def __get_other_targets__(self): return tuple(self.__other_targets__)
    other_targets = property(__get_other_targets__, doc="the other targets of this %s action" % (BangActionType.other))


###################### add all skill actions ##########################
Single_Skills = [
CharacterCardNames.Bart_Cassidy,
CharacterCardNames.Calamity_Janet,
CharacterCardNames.EI_Gringo,
CharacterCardNames.Jesse_Jones,
CharacterCardNames.Jourdonnais,
CharacterCardNames.Paul_Regret,
CharacterCardNames.Pedro_Ramirez,
CharacterCardNames.Rose_Doolan,
CharacterCardNames.Slab_Killer,
CharacterCardNames.Suzy_Lafayette,
CharacterCardNames.Vulture_Sam,
CharacterCardNames.Willy_Kid
]
for skill in Single_Skills:
    AllBangActionsDict[skill] = BangAction(skill)
    AllBangActionsDict[skill].__is_public__ = True

#13
'''
Black Jack = Tom Ketchum (known as Black Jack) – During phase 1 of his turn, he must show the second normal card he draws: if it's a Heart or Diamond, he draws one additional normal card that turn (without revealing it).\n\n
The key of Black_Jack_BangAction is CharacterCardNames.Black_Jack-secondcard.key \n
The character of Black_Jack_BangAction is CharacterCardNames.Black_Jack \n
'''
for playingcard in AllPlayingCardsDict:
    key = CharacterCardNames.Black_Jack + "-" + playingcard.key
    AllBangActionsDict[key] = BangAction(key)
    AllBangActionsDict[key].__is_public__ = True

#14
'''
Kit Carlson = Kit Carson – During the phase 1 of his turn, he looks at the top three cards of the deck: he chooses 2 to draw, and puts the other one back on the top of the deck, face down. 
'''
for i in range(len(ADeckOfCards)):
    for j in range(len(ADeckOfCards)):
        for k in range(len(ADeckOfCards)):
            if i != j and i != k and j != k:
                key = CharacterCardNames.Kit_Carlso + "-"+":".join(
                    [c.key for c in sorted([ADeckOfCards[i], ADeckOfCards[j], ADeckOfCards[k]], key=lambda x:x.key)]) + "-" +":".join(
                    [c.key for c in sorted([ADeckOfCards[i], ADeckOfCards[j]], key=lambda x:x.key)])
                AllBangActionsDict[key] = BangAction(key)
                AllBangActionsDict[key].__is_public__ = False

                key = CharacterCardNames.Kit_Carlso + "-" + ":".join(
                    [c.key for c in sorted([ADeckOfCards[i], ADeckOfCards[j], ADeckOfCards[k]], key=lambda x: x.key)]) + "-" + ":".join(
                    [c.key for c in sorted([ADeckOfCards[i], ADeckOfCards[k]], key=lambda x: x.key)])
                AllBangActionsDict[key] = BangAction(key)
                AllBangActionsDict[key].__is_public__ = False

                key = CharacterCardNames.Kit_Carlso + "-" + ":".join(
                    [c.key for c in sorted([ADeckOfCards[i], ADeckOfCards[j], ADeckOfCards[k]], key=lambda x: x.key)]) + "-" + ":".join(
                    [c.key for c in sorted([ADeckOfCards[j], ADeckOfCards[k]], key=lambda x: x.key)])
                AllBangActionsDict[key] = BangAction(key)
                AllBangActionsDict[key].__is_public__ = False


#15
'''
Lucky Duke = Lucky Luke (Fictional person) – Each time he is required to "draw!", he flips the top two cards from the deck, and chooses the result he prefers. Discard both cards afterward. 
'''
for i in range(len(ADeckOfCards)):
        for j in range(i + 1, len(ADeckOfCards)):
                key = CharacterCardNames.Lucky_Duke + "-" + ":".join(
                    [c.key for c in sorted([ADeckOfCards[i], ADeckOfCards[j]], key=lambda x:x.key)]) + "-"+ ADeckOfCards[i].key
                AllBangActionsDict[key] = BangAction(key)
                AllBangActionsDict[key].__is_public__ = True

#16
'''
Sid Ketchum = Tom Ketchum – At any time, he may discard 2 cards from his hand to regain one life point. If he is willing and able, he can use this ability more than once at a time. 
'''
for i in range(len(ADeckOfCards)):
    for j in range(len(ADeckOfCards)):
        key = CharacterCardNames.Sid_Ketchum + "-" + ":".join(
                    [c.key for c in sorted([ADeckOfCards[i], ADeckOfCards[j]], key=lambda x:x.key)])
        AllBangActionsDict[key] = BangAction(key)
        AllBangActionsDict[key].__is_public__ = True


###################### add all card actions  ##########################
for playingcard in AllPlayingCardsDict:
    if playingcard.name == PlayingCardNames.Duello: #决斗
        for i in range(5):
            AllBangActionsDict[playingcard.key+"-%d"%(i)] = BangAction(playingcard.key+"-%d"%(i))
            AllBangActionsDict[playingcard.key + "-%d" % (i)].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Bang: # 杀
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
        for i in range(5):
            AllBangActionsDict[playingcard.key+"-%d"%(i)] = BangAction(playingcard.key+"-%d"%(i))
            AllBangActionsDict[playingcard.key + "-%d" % (i)].__is_public__ = True
    elif playingcard.name == PlayingCardNames.StageCoach:
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Indian: ##   南蛮入侵
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Miss: ## 闪
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Panic: ## 顺手牵羊
        for i in range(5):
            AllBangActionsDict[playingcard.key+"-%d"%(i)] = BangAction(playingcard.key+"-%d"%(i))
            AllBangActionsDict[playingcard.key + "-%d" % (i)].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Barrel: ## 八卦阵
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Dynamite: ## 闪电
        for i in range(5):
            AllBangActionsDict[playingcard.key+"-%d"%(i)] = BangAction(playingcard.key+"-%d"%(i))
            AllBangActionsDict[playingcard.key + "-%d" % (i)].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Beer: ## 桃
        for i in range(5):
            AllBangActionsDict[playingcard.key+"-%d"%(i)] = BangAction(playingcard.key+"-%d"%(i))
            AllBangActionsDict[playingcard.key + "-%d" % (i)].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Catling: #万箭齐发
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Saloon: ## 全体加一血，桃园结义
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.CatBalou: ## 过河拆桥
        for i in range(5):
            AllBangActionsDict[playingcard.key+"-%d"%(i)] = BangAction(playingcard.key+"-%d"%(i))
            AllBangActionsDict[playingcard.key + "-%d" % (i)].__is_public__ = True
    elif playingcard.name == PlayingCardNames.WellsFargo: ##  多从牌库抽三张牌
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard == PlayingCardNames.Jail: ## 乐不思蜀
        AllBangActionsDict[playingcard.key+"-%d"%(i)] = BangAction(playingcard.key+"-%d"%(i))
        AllBangActionsDict[playingcard.key + "-%d" % (i)].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Emporia: #計算目前仍在遊戲中的人數，從牌庫翻開相同數量的牌，每位玩家挑選一張價入自己的手牌中。
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True



    elif playingcard.name == PlayingCardNames.Mustang: #horse
        AllBangActionsDict[playingcard.key] =  BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Appaloosa: ## horse
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True


    elif playingcard.name == PlayingCardNames.Remington: ## guns
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Volcanic: ## guns
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Schofield: ## guns
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Carabine: #guns
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
        AllBangActionsDict[playingcard.key].__is_public__ = True
    elif playingcard.name == PlayingCardNames.Winchester: #guns
        AllBangActionsDict[playingcard.key] = BangAction(playingcard.key)
    AllBangActionsDict[playingcard.key].__is_public__ = True

################# add other actions
AllBangActionsDict[OtherActionNames.giveup] = BangAction(OtherActionNames.giveup)
AllBangActionsDict[playingcard.key].__is_public__ = True
for playingcard in AllPlayingCardsDict:
    key = "%s_%s"%(OtherActionNames.emporiachoose,playingcard.key)
    AllBangActionsDict[key] = BangAction(key)
    AllBangActionsDict[playingcard.key].__is_public__ = False
AllBangActionsDict[OtherActionNames.draw] = BangAction(OtherActionNames.draw)
AllBangActionsDict[playingcard.key].__is_public__ = True