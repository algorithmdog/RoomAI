#!/bin/python
#coding:utf-8

from roomai.games.common import AbstractAction
from roomai.games.bang import AllPlayingCardsDict
from roomai.games.bang import PlayingCardNames
from roomai.games.bang import CharacterCardNames
import roomai



class Bart_Cassidy_BangAction(AbstractAction):
    '''
    Bart Cassidy = Butch Cassidy – Each time he loses a life point, he immediately draws a normal card from the deck. \n\n
    The key of Bart_Cassidy_BangAction is CharacterCardNames.Bart_Cassidy \n
    The character of Bart_Cassidy_BangAction is CharacterCardNames.Bart_Cassidy \n
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Bart_Cassidy
        self.__character__ = CharacterCardNames.Black_Jack

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.Bart_Cassidy ")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Black_Jack_SkillActon(AbstractAction):
    '''
    Black Jack = Tom Ketchum (known as Black Jack) – During phase 1 of his turn, he must show the second normal card he draws: if it's a Heart or Diamond, he draws one additional normal card that turn (without revealing it).\n\n
    The key of Black_Jack_BangAction is CharacterCardNames.Black_Jack-secondcard.key \n
    The character of Black_Jack_BangAction is CharacterCardNames.Black_Jack \n
    '''
    def __init__(self, second_card):
        self.__key__ = CharacterCardNames.Black_Jack + "-" + second_card.key
        self.__second_card__ = second_card
        self.__character__ = CharacterCardNames.Black_Jack

    def __get_second_card__(self):   return self.__second_card__
    second_card = property(__get_second_card__, doc="During phase 1 of Black Jack turn, Black Jack must show the second normal card he draws")

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.Black_Jack")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Calamity_Janet_BangAction(AbstractAction):
    '''
    Calamity Janet = Calamity Jane – She can use "Bang!" cards as "Missed!" cards and vice versa. She is still subject to "Bang!" limitations: If she plays a Missed! normal card as a "Bang!", she cannot play another "Bang!" normal card that turn (unless she has a Volcanic in play). (4 life points)\n\n
    The key of Black_Jack_BangAction is CharacterCardNames.Calamity_Janet \n
    The character of Black_Jack_BangAction is CharacterCardNames.Calamity_Janet \n
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Calamity_Janet
        self.__character__ = CharacterCardNames.Calamity_Janet

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is  CharacterCardNames.Calamity_Janet ")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class EI_Gringo_BangAction(AbstractAction):
    '''
    El Gringo = gringo (slang Spanish word) – Each time he loses a life point due to a normal card played by another player, he draws a random normal card from the hands of that player (one normal card for each life). If the player has no more cards, he does not draw. (3 life points)
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.EI_Gringo
        self.__character__ = CharacterCardNames.EI_Gringo

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.EI_Gringo ")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Jesse_Jones_BangAction(AbstractAction):
    '''
    Jesse Jones = Jesse James – During phase 1 of his turn, he may choose to draw the first normal card from the deck, or randomly from the hand of any other player. Then he draws the second normal card from the deck. 
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Jesse_Jones
        self.__character__ = CharacterCardNames.Jesse_Jones

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.Jesse_Jones")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Jourdonnais_BangAction(AbstractAction):
    '''
    Jourdonnais = "Frenchy" Jourdonnais, the riverboat captain in The Big Sky novel and movie (Fictional person) – He is considered to have Barrel in play at all times; he can "draw!" when he is the target of a BANG!, and on a Heart he is missed. 
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Jourdonnais
        self.__character__ = CharacterCardNames.Jourdonnais

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.Jourdonnais ")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]


class Kit_Carlson_BangAction(AbstractAction):
    '''
    Kit Carlson = Kit Carson – During the phase 1 of his turn, he looks at the top three cards of the deck: he chooses 2 to draw, and puts the other one back on the top of the deck, face down. 
    '''
    def __init__(self, top1card, top2card, top3card, choose1card, choose2card):
        topcards = [top1card, top2card, top3card]
        self.__sorted_topcards__ = sorted(topcards, key=lambda x: x.key)

        choosecards = [choose1card, choose2card]
        self.__sorted_choosecards__ = sorted(choosecards, key = lambda x:x.key)

        self.__key__ = CharacterCardNames.Kit_Carlson + "-" + self.sorted_topcards[0].key + "-" +self.sorted_topcards[1].key + "-" + self.sorted_topcards[2].key + "-" + self.sorted_choosecards[0].key + "-" + self.sorted_choosecards[1].key
        self.__character__ = CharacterCardNames.Kit_Carlson

    def __get_sorted_topcards__(self): return tuple(self.__sorted_choosecards__)
    sorted_topcards = property(__get_sorted_topcards__, doc="top three cards of the deck")

    def __get_sorted_choosecards__(self): return tuple(self.__sorted_choosecards__)
    sorted_choosecards = property(__get_sorted_topcards__, doc="the choosen 2 cards")

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is Kit_Carlson_BangAction")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]


class Lucky_Duke_BangAction(AbstractAction):
    '''
    Lucky Duke = Lucky Luke (Fictional person) – Each time he is required to "draw!", he flips the top two cards from the deck, and chooses the result he prefers. Discard both cards afterward. 
    '''
    def __init__(self, top1card, top2card, choose1card):
        topcards = [top1card, top2card]
        self.__sorted_topcards__ = sorted(topcards, key=lambda x: x.key)

        choosecards = [choose1card]
        self.__sorted_choosecards__ = sorted(choosecards, key = lambda x:x.key)

        self.__key__ = CharacterCardNames.Lucky_Duke + "-" + self.sorted_topcards[0].key + "-" +self.sorted_topcards[1].key + "-" + self.sorted_choosecards[0].key
        self.__character__ = CharacterCardNames.Lucky_Duke

    def __get_sorted_topcards__(self): return tuple(self.__sorted_choosecards__)
    sorted_topcards = property(__get_sorted_topcards__, doc="top 2 cards of the deck")

    def __get_sorted_choosecards__(self): return tuple(self.__sorted_choosecards__)
    sorted_choosecards = property(__get_sorted_topcards__, doc="the choosen 1 cards")

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is Lucky_Duke")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Paul_Regret_BangAction(AbstractAction):
    '''
    Paul Regret = Paul Regret – The Comancheros (film) – He is considered to have a Mustang in play at all times; all other players must add 1 to the distance to him. If he has another real Mustang in play, he can count both of them, increasing all distance to him by a total of 2.
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Paul_Regret
        self.__character__ = CharacterCardNames.Paul_Regret

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.Paul_Regret ")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Pedro_Ramirez(AbstractAction):
    '''
    Pedro Ramirez = Tuco Ramirez – The Ugly in the film The Good, the Bad and the Ugly (Fictional person) – During phase 1 of his turn, he may choose to draw the first card from the top of the discard pile or from the deck. Then he draws the second normalcard from the deck. 
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Pedro_Ramirez
        self.__character__ = CharacterCardNames.Pedro_Ramirez

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.Pedro_Ramirez ")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]


class Rose_Doolan(AbstractAction):
    '''
    Rose Doolan = She is considered to have a Scope (Appaloosa in older versions) in play at all times; she sees the other players at a distance decreased by 1. If she has another real Scope in play, she can count both of them, reducing her distance to all other players by a total of 2. 
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Rose_Doolan
        self.__character__ = CharacterCardNames.Rose_Doolan

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is CharacterCardNames.Rose_Doolan ")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Sid_Ketchum_BangAction(AbstractAction):
    '''
    Sid Ketchum = Tom Ketchum – At any time, he may discard 2 cards from his hand to regain one life point. If he is willing and able, he can use this ability more than once at a time. 
    '''
    def __init__(self, card1, card2):
        cards = [card1, card2]
        self.__cards__ = sorted(cards, key=lambda x: x.key)


        self.__key__ = CharacterCardNames.Sid_Ketchum + "-" + self.cards[0].key + "-" +self.cards[1].key
        self.__character__ = CharacterCardNames.Sid_Ketchum

    def __get_cards__(self): return tuple(self.__cards__)
    sorted_topcards = property(__get_cards__, doc="discarded two cards")


    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is Sid_Ketchum")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]


class Slab_Killer_BangAction(AbstractAction):
    '''
    Slab the Killer = Angel Eyes, the Bad in the film The Good, the Bad and the Ugly (Fictional person) – Players trying to cancel his BANG! cards need to play 2 Missed!. The Barrel effect, if successfully used, only counts as one Missed! 
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Slab_Killer
        self.__character__ = CharacterCardNames.Slab_Killer

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is Slab_Killer")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]

class Suzy_Lafayette_BangAction(AbstractAction):
    '''
    Suzy Lafayette = As soon as she has no cards in her hand, she instantly draws a normal card from the draw pile. 
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Suzy_Lafayette
        self.__character__ = CharacterCardNames.Suzy_Lafayette

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is Suzy_Lafayette")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]


class Vulture_Sam_BangAction(AbstractAction):
    '''
    Vulture Sam = Whenever a character is eliminated from the game, Sam takes all the cards that player had in his hand and in play, and adds them to his hand
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Vulture_Sam
        self.__character__ = CharacterCardNames.Vulture_Sam

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is Vulture_Sam")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]


class Willy_Kid_BangAction(AbstractAction):
    '''
    Vulture Sam = Whenever a character is eliminated from the game, Sam takes all the cards that player had in his hand and in play, and adds them to his hand
    '''
    def __init__(self):
        self.__key__ = CharacterCardNames.Willy_Kid
        self.__character__ = CharacterCardNames.Willy_Kid

    def __get_character_(self): return self.__character__
    character = property(__get_character_, doc="which character this skill action belongs to. Now it is Willy_Kid")

    def __deepcopy__(self, memodict={}):
        return AllBangActionsDict[self.key]




class BangAction(AbstractAction):
    '''
    BangAction is the action played by the normal players \n\n
    The action key looks like "cardkey_firsttarget(option)_secondtarget(option)"
    
    
    '''
    def __init__(self, key):
        logger = roomai.get_logger()
        self.__card__ = None
        self.__first_target__ = None
        self.__second_target__ = None
        self.__key__ = None

        keys = key.split("_")
        if keys[0] in AllPlayingCardsDict:
            self.__card__ = AllPlayingCardsDict[keys[0]]
        else:
            logger.info("%s is invalid action key, since the cardkey %s is invalid"%(key, keys[0]))




    @classmethod
    def lookup(self, key):
        raise NotImplementedError

    def __get_card__(self): return self.__card__
    card = property(__get_card__, doc="the card used in this action")



    def __get_source__(self): return self.__source__
    source = property(__get_source__, doc="the id of the player, who issues this action")

    def __get_first_target__(self): return self.__first_target__
    first_target = property(__get_first_target__,doc = "the first target of this action")

    def __get_second_target__(self): return self.__second_target__
    second_target = property(__get_second_target__, doc = "the second target of this action")



AllBangActionsDict = dict()
for playingcard in AllPlayingCardsDict:
    if playingcard.name == PlayingCardNames.Duello:

        AllPlayingCardsDict[playingcard.key] = action

    elif card.name == PlayingCardNames.Carabine:
        pass
    elif card.name == PlayingCardNames.Bang:
        pass
    elif card.name == PlayingCardNames.Emporia:
        pass
    elif card.name == PlayingCardNames.Volcanic:
        pass
    elif card.name == PlayingCardNames.Schofield:
        pass
    elif card.name == PlayingCardNames.Remington:
        pass
    elif card.name == PlayingCardNames.Panic:
        pass
    elif card.name == PlayingCardNames.Dynamite:
        pass
    elif card.name == PlayingCardNames.WellsFargo:
        pass
    elif card.name == PlayingCardNames.Prigione:
        pass
    elif card.name == PlayingCardNames.Saloon:
        pass
    elif card.name == PlayingCardNames.Beer:
        pass
    elif card.name == PlayingCardNames.Catling:
        pass
    elif card.name == PlayingCardNames.CatBalou:
        pass
    elif card.name == PlayingCardNames.Miss:
        pass
    elif card.name == PlayingCardNames.StageCoach:
        pass
    elif card.name == PlayingCardNames.Barrel:
        pass
    elif card.name == PlayingCardNames.Mustang:
        pass
    elif card.name == PlayingCardNames.Indian:
        pass
    elif card.name == PlayingCardNames.Winchester:
        pass
    elif card.name == PlayingCardNames.Appaloosa:
        pass