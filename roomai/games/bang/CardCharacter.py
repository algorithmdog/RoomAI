#!/bin/python

import roomai

class CharacterCardNames:
    Bart_Cassidy   = "Bart_Cassidy"
    #Bart Cassidy = Butch Cassidy – Each time he loses a life point, he immediately draws a normal card from the deck. (4 life points)
    Black_Jack     = "Black_Jack"
    #Black Jack = Tom Ketchum (known as Black Jack) – During phase 1 of his turn, he must show the second normal card he draws: if it's a Heart or Diamond, he draws one additional normalcard that turn (without revealing it). (4 life points)
    Calamity_Janet = "Calamity_Janet"
    #Calamity Janet = Calamity Jane – She can use "Bang!" cards as "Missed!" cards and vice versa. She is still subject to "Bang!" limitations: If she plays a Missed! normalcard as a "Bang!", she cannot play another "Bang!" normalcard that turn (unless she has a Volcanic in play). (4 life points)
    EI_Gringo      = "EI_Gringo"
    #El Gringo = gringo (slang Spanish word) – Each time he loses a life point due to a normalcard played by another player, he draws a random normalcard from the hands of that player (one normalcard for each life). If the player has no more cards, he does not draw. (3 life points)
    Jesse_Jones    = "Jesse_Jones"
    #Jesse Jones = Jesse James – During phase 1 of his turn, he may choose to draw the first normalcard from the deck, or randomly from the hand of any other player. Then he draws the second normalcard from the deck. (4 life points)
    Jourdonnais    = "Jourdonnais"
    #Jourdonnais = "Frenchy" Jourdonnais, the riverboat captain in The Big Sky novel and movie (Fictional person) – He is considered to have Barrel in play at all times; he can "draw!" when he is the target of a BANG!, and on a Heart he is missed. If he has another real Barrel normalcard in play he can count both of them, giving him two chances to cancel the BANG! before playing a Missed! (4 life points)
    Kit_Carlson    = "Kit_Carlson"
    #Kit Carlson = Kit Carson – During the phase 1 of his turn, he looks at the top three cards of the deck: he chooses 2 to draw, and puts the other one back on the top of the deck, face down. (4 life points)
    Lucky_Duke     = "Lucky_Duke"
    #Lucky Duke = Lucky Luke (Fictional person) – Each time he is required to "draw!", he flips the top two cards from the deck, and chooses the result he prefers. Discard both cards afterward. (4 life points)
    Paul_Regret    = "Paul_Regret"
    #Paul Regret = Paul Regret – The Comancheros (film) – He is considered to have a Mustang in play at all times; all other players must add 1 to the distance to him. If he has another real Mustang in play, he can count both of them, increasing all distance to him by a total of 2. (3 life points)
    Pedro_Ramirez  = "Pedro_Ramirez"
    #Pedro Ramirez = Tuco Ramirez – The Ugly in the film The Good, the Bad and the Ugly (Fictional person) – During phase 1 of his turn, he may choose to draw the first card from the top of the discard pile or from the deck. Then he draws the second normalcard from the deck. (4 life points)
    Rose_Doolan    = "Rose_Doolan"
    #Rose Doolan = She is considered to have a Scope (Appaloosa in older versions) in play at all times; she sees the other players at a distance decreased by 1. If she has another real Scope in play, she can count both of them, reducing her distance to all other players by a total of 2. (4 life points)
    Sid_Ketchum    = "Sid_Ketchum"
    #Sid Ketchum = Tom Ketchum – At any time, he may discard 2 cards from his hand to regain one life point. If he is willing and able, he can use this ability more than once at a time. (4 life points)
    Slab_Killer    = "Slab_Killer"
    #Slab the Killer = Angel Eyes, the Bad in the film The Good, the Bad and the Ugly (Fictional person) – Players trying to cancel his BANG! cards need to play 2 Missed!. The Barrel effect, if successfully used, only counts as one Missed! (4 life points)
    Suzy_Lafayette = "Suzy_Lafayette"
    #Suzy Lafayette = As soon as she has no cards in her hand, she instantly draws a normalcard from the draw pile. (4 life points)
    Vulture_Sam    = "Vulture_Sam"
    #Vulture Sam = Whenever a character is eliminated from the game, Sam takes all the cards that player had in his hand and in play, and adds them to his hand. (4 life points)
    Willy_Kid      = "Willy_Kid"
    #Willy the Kid = Billy the Kid – He can play any number of "Bang!" cards. (4 life points)

class CharacterCard(object):

    def __init__(self, character, hp):
        self.__hp__   = hp
        self.__key__  = character
        self.__name1__ = character


    def __get_name__(self):
        return self.__name1__
    name = property(__get_name__, doc="The person name of character card")

    def __get_hp__(self):
        return self.__hp__
    hp = property(__get_hp__, doc = "The init hp of this character card")

    def __get_key__(self):  return self.__key__
    key = property(__get_key__, doc = "The key of this character card")

    def __deepcopy__(self, memodict={}):
        return AllCharacterCardsDict[self.__key__]

    @classmethod
    def lookup(cls,key):
        logger = roomai.get_logger()
        if key not in AllCharacterCardsDict:
            logger.fatal("key (%s) is not invalid charactor key" % (key))
            raise ValueError("key (%s) is not invalid charactor key" % (key))
        return AllCharacterCardsDict[key]

AllCharacterCardsDict = dict()
AllCharacterCardsDict[CharacterCardNames.Jesse_Jones] = CharacterCard(CharacterCardNames.Jesse_Jones, 4)
AllCharacterCardsDict[CharacterCardNames.Vulture_Sam] = CharacterCard(CharacterCardNames.Vulture_Sam, 4)
AllCharacterCardsDict[CharacterCardNames.Bart_Cassidy] = CharacterCard(CharacterCardNames.Bart_Cassidy, 4)
AllCharacterCardsDict[CharacterCardNames.Calamity_Janet] = CharacterCard(CharacterCardNames.Calamity_Janet, 4)
AllCharacterCardsDict[CharacterCardNames.Black_Jack]  = CharacterCard(CharacterCardNames.Black_Jack, 4)
AllCharacterCardsDict[CharacterCardNames.Jourdonnais] = CharacterCard(CharacterCardNames.Jourdonnais, 4)
AllCharacterCardsDict[CharacterCardNames.Kit_Carlson] = CharacterCard(CharacterCardNames.Kit_Carlson, 4)
AllCharacterCardsDict[CharacterCardNames.Rose_Doolan] = CharacterCard(CharacterCardNames.Rose_Doolan, 4)
AllCharacterCardsDict[CharacterCardNames.Suzy_Lafayette] = CharacterCard(CharacterCardNames.Suzy_Lafayette, 4)
AllCharacterCardsDict[CharacterCardNames.Sid_Ketchum] = CharacterCard(CharacterCardNames.Sid_Ketchum, 4)
AllCharacterCardsDict[CharacterCardNames.EI_Gringo] = CharacterCard(CharacterCardNames.EI_Gringo, 3)
AllCharacterCardsDict[CharacterCardNames.Lucky_Duke] = CharacterCard(CharacterCardNames.Lucky_Duke, 4)
AllCharacterCardsDict[CharacterCardNames.Slab_Killer] = CharacterCard(CharacterCardNames.Slab_Killer, 4)
AllCharacterCardsDict[CharacterCardNames.Paul_Regret] = CharacterCard(CharacterCardNames.Paul_Regret, 3)
AllCharacterCardsDict[CharacterCardNames.Pedro_Ramirez] = CharacterCard(CharacterCardNames.Pedro_Ramirez, 4)
AllCharacterCardsDict[CharacterCardNames.Willy_Kid] = CharacterCard(CharacterCardNames.Willy_Kid, 4)
