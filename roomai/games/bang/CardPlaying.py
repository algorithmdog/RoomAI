#!/bin/python

import roomai

class PlayingCardNames:
    Duello      = "Duello"
    Carabine    = "Carabine"
    Bang        = "Bang"
    Emporia     = "Emporia"
    Volcanic    = "Volcanic"
    Schofield   = "Schofield"
    Remington   = "Remington"
    Panic       = "Panic"
    Dynamite    = "Dynamite"
    WellsFargo  = "WellsFargo"
    Jail        = "Jail"
    Saloon      = "Saloon"
    Beer        = "Beer"
    Catling     = "Catling"
    CatBalou    = "CatBalou"
    Miss        = "Miss"
    StageCoach  = "StageCoach"
    Barrel      = "Barrel"
    Mustang     = "Mustang"
    Indian      = "Indian"
    Winchester  = "Winchester"
    Appaloosa   = "Appaloosa"


class PlayingCardSuits:
    Club    = "Club"
    Heart   = "Heart"
    Diamond = "Diamond"
    Spade   = "Spade"

class PlayingCardColors:
    Blue = "Blue"
    Brown = "Brown"


class PlayingCard(object):
    '''
    A Poker Card. \n
    A Poker Card has a point (A,2,3,4,....,K) and a suit (Spade, Heart, Diamond, Club). \n
    Different points have different ranks, for example the point 2's rank is 0, and the point A's rank is 12. \n
    Different suits have different ranks too. \n
    A Poker Card has a key (point_suit). We strongly recommend you to get a poker normalcard by using the class function lookup with the key. \n
    Examples of the class usages: \n
    >> import roomai.games.texasholdem \n
    >> normalcard = roomai.games.texasholdem.Card.lookup("2_Spade") \n
    >> normalcard.point \n
    2\n
    >> normalcard.suit\n
    Spade\n
    >> normalcard.point_rank\n
    0\n
    >> normalcard.suit_rank\n
    0\n
    >> normalcard.key\n
    "2_Spade"\n
    '''


    def __init__(self, card, point, suit, color):

        self.__point__      = point
        self.__suit__       = suit
        self.__name1__      = card
        self.__color__      = color
        self.__key__        = "%s-%s-%s" % (self.__card__, self.__point__, self.__suit__)

    def __get_point__(self):
        return self.__point__
    point = property(__get_point__, doc="The point of the playing card")

    def __get_suit__(self):
        return self.__suit__
    suit = property(__get_suit__, doc="The suit of the playing card")

    def __get_name__(self):
        return self.__name1__
    name = property(__get_name__, doc="the name of the playing card")

    def __get_color__(self):
        return self.__color__
    color = property(__get_color__, doc = "the border color of the playing card")

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the playing card")


    @classmethod
    def lookup(cls, key):
        '''
        lookup a Card with the specified key

        :param key: The specified key
        :return: The Card with the specified key
        '''

        logger = roomai.get_logger()
        if key not in AllPlayingCardsDict:
            logger.fatal("key (%s) is not invalid poker normalcard key"%(key))
            raise ValueError("key (%s) is not invalid poker normalcard key"%(key))

        return AllPlayingCardsDict[key]


    def __deepcopy__(self, memodict={}):
        return AllPlayingCardsDict[self.key]

AllPlayingCardsDict = dict()
###############################
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Carabine, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Carabine, "A", PlayingCardSuits.Club, PlayingCardColors.Blue)
for i in range(2,8):
    AllPlayingCardsDict["%s-%d-%s" % (PlayingCardNames.Duello, i, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Bang, "%d" % (i), PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-8-%s" % (PlayingCardNames.Duello, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Duello, "8", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-9-%s" % (PlayingCardNames.Emporia, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Emporia, "9", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-10-%s" % (PlayingCardNames.Volcanic, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Volcanic, "10", PlayingCardSuits.Club, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.Schofield, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Schofield, "J", PlayingCardSuits.Club, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Schofield, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Schofield, "Q", PlayingCardSuits.Club, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-K-%s" % (PlayingCardNames.Remington, PlayingCardSuits.Club)] = PlayingCard(PlayingCardNames.Remington, "K", PlayingCardSuits.Club, PlayingCardColors.Blue)


###############################
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Panic, PlayingCardSuits.Heart)]          = PlayingCard(PlayingCardNames.Panic, "A", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-2-%s" % (PlayingCardNames.Dynamite, PlayingCardSuits.Heart)]       = PlayingCard(PlayingCardNames.Dynamite, "2", PlayingCardSuits.Heart, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-3-%s" % (PlayingCardNames.WellsFargo, PlayingCardSuits.Heart)]     = PlayingCard(PlayingCardNames.WellsFargo, "3", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-4-%s" % (PlayingCardNames.Prigione, PlayingCardSuits.Heart)]       = PlayingCard(PlayingCardNames.Prigione, "4", PlayingCardSuits.Heart, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-5-%s" % (PlayingCardNames.Saloon, PlayingCardSuits.Heart)]         = PlayingCard(PlayingCardNames.Saloon, "5", PlayingCardSuits.Heart, PlayingCardColors.Brown)

for i in range(6,10):
    AllPlayingCardsDict["%s-%d-%s" % (PlayingCardNames.Beer, i, PlayingCardSuits.Heart)]  = PlayingCard(PlayingCardNames.Beer, "%d" % (i), PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-10-%s" % (PlayingCardNames.Catling, PlayingCardSuits.Heart)]       = PlayingCard(PlayingCardNames.Catling, "10", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.Beer, PlayingCardSuits.Heart)]           = PlayingCard(PlayingCardNames.Beer, "J", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Heart)]           = PlayingCard(PlayingCardNames.Bang, "Q", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.CatBalou, PlayingCardSuits.Heart)]       = PlayingCard(PlayingCardNames.CatBalou, "K", PlayingCardSuits.Heart, PlayingCardColors.Brown)


#################################
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Spade)]          = PlayingCard(PlayingCardNames.Bang, "A", PlayingCardSuits.Spade, PlayingCardColors.Brown)
for i in range(2,9):
    AllPlayingCardsDict["%s-%d-%s" % (PlayingCardNames.Miss, i, PlayingCardSuits.Spade)]  = PlayingCard(PlayingCardNames.Miss, "%d" % (i), PlayingCardSuits.Spade, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-9-%s" % (PlayingCardNames.StageCoach, PlayingCardSuits.Spade)]     = PlayingCard(PlayingCardNames.StageCoach, "9", PlayingCardSuits.Spade, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-10-%s" % (PlayingCardNames.Prigione, PlayingCardSuits.Spade)]      = PlayingCard(PlayingCardNames.Prigione, "10", PlayingCardSuits.Spade, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.Prigione, PlayingCardSuits.Spade)]       = PlayingCard(PlayingCardNames.Prigione, "J", PlayingCardSuits.Spade, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Barrel, PlayingCardSuits.Spade)]       = PlayingCard(PlayingCardNames.Barrel, "Q", PlayingCardSuits.Spade, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-K-%s" % (PlayingCardNames.Schofield, PlayingCardSuits.Spade)]       = PlayingCard(PlayingCardNames.Schofield, "K", PlayingCardSuits.Spade, PlayingCardColors.Blue)


#######################################
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Diamond)]          = PlayingCard(PlayingCardNames.Bang, "A", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
for i in range(2,11):
    AllPlayingCardsDict["%s-%d-%s" % (PlayingCardNames.Bang, i, PlayingCardSuits.Diamond)]  = PlayingCard(PlayingCardNames.Bang, "%d" % (i), PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Diamond)]       = PlayingCard(PlayingCardNames.Bang, "J", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Diamond)]       = PlayingCard(PlayingCardNames.Bang, "Q", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-K-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Diamond)]       = PlayingCard(PlayingCardNames.Bang, "K", PlayingCardSuits.Diamond, PlayingCardColors.Brown)




##########################################
AllPlayingCardsDict["%s-8-%s" % (PlayingCardNames.Mustang, PlayingCardSuits.Heart)]   = PlayingCard(PlayingCardNames.Mustang, "8", PlayingCardSuits.Heart, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-9-%s" % (PlayingCardNames.Mustang, PlayingCardSuits.Heart)]   = PlayingCard(PlayingCardNames.Mustang, "9", PlayingCardSuits.Heart, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-10-%s" % (PlayingCardNames.Beer, PlayingCardSuits.Heart)]     = PlayingCard(PlayingCardNames.Beer, "10", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.Panic, PlayingCardSuits.Heart)]     = PlayingCard(PlayingCardNames.Panic, "J", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Panic, PlayingCardSuits.Heart)]     = PlayingCard(PlayingCardNames.Panic, "Q", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-K-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Heart)]      = PlayingCard(PlayingCardNames.Bang, "K", PlayingCardSuits.Heart, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Heart)]      = PlayingCard(PlayingCardNames.Bang, "A", PlayingCardSuits.Heart, PlayingCardColors.Brown)


AllPlayingCardsDict["%s-8-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Club)]      = PlayingCard(PlayingCardNames.Bang, "8", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-9-%s" % (PlayingCardNames.Bang, PlayingCardSuits.Club)]      = PlayingCard(PlayingCardNames.Bang, "9", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-10-%s" % (PlayingCardNames.Miss, PlayingCardSuits.Club)]     = PlayingCard(PlayingCardNames.Miss, "10", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.Miss, PlayingCardSuits.Club)]      = PlayingCard(PlayingCardNames.Miss, "J", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Miss, PlayingCardSuits.Club)]      = PlayingCard(PlayingCardNames.Miss, "Q", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-K-%s" % (PlayingCardNames.Miss, PlayingCardSuits.Club)]      = PlayingCard(PlayingCardNames.Miss, "K", PlayingCardSuits.Club, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Miss, PlayingCardSuits.Club)]      = PlayingCard(PlayingCardNames.Miss, "A", PlayingCardSuits.Club, PlayingCardColors.Brown)


AllPlayingCardsDict["%s-8-%s" % (PlayingCardNames.Panic, PlayingCardSuits.Diamond)]           = PlayingCard(PlayingCardNames.Panic, "8", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-9-%s" % (PlayingCardNames.CatBalou, PlayingCardSuits.Diamond)]        = PlayingCard(PlayingCardNames.CatBalou, "9", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-10-%s" % (PlayingCardNames.CatBalou, PlayingCardSuits.Diamond)]       = PlayingCard(PlayingCardNames.CatBalou, "10", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.CatBalou, PlayingCardSuits.Diamond)]        = PlayingCard(PlayingCardNames.CatBalou, "J", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Duello, PlayingCardSuits.Diamond)]          = PlayingCard(PlayingCardNames.Duello, "Q", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-K-%s" % (PlayingCardNames.Indian, PlayingCardSuits.Diamond)]          = PlayingCard(PlayingCardNames.Indian, "K", PlayingCardSuits.Diamond, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Indian, PlayingCardSuits.Diamond)]          = PlayingCard(PlayingCardNames.Indian, "A", PlayingCardSuits.Diamond, PlayingCardColors.Brown)


AllPlayingCardsDict["%s-8-%s" % (PlayingCardNames.Winchester, PlayingCardSuits.Spade)]        = PlayingCard(PlayingCardNames.Winchester, "8", PlayingCardSuits.Spade, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-9-%s" % (PlayingCardNames.StageCoach, PlayingCardSuits.Spade)]        = PlayingCard(PlayingCardNames.StageCoach, "9", PlayingCardSuits.Spade, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-10-%s" % (PlayingCardNames.Volcanic, PlayingCardSuits.Spade)]         = PlayingCard(PlayingCardNames.Volcanic, "10", PlayingCardSuits.Spade, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-J-%s" % (PlayingCardNames.Duello, PlayingCardSuits.Spade)]            = PlayingCard(PlayingCardNames.Duello, "J", PlayingCardSuits.Spade, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-Q-%s" % (PlayingCardNames.Emporia, PlayingCardSuits.Spade)]           = PlayingCard(PlayingCardNames.Emporia, "Q", PlayingCardSuits.Spade, PlayingCardColors.Brown)
AllPlayingCardsDict["%s-K-%s" % (PlayingCardNames.Barrel, PlayingCardSuits.Spade)]            = PlayingCard(PlayingCardNames.Barrel, "K", PlayingCardSuits.Spade, PlayingCardColors.Blue)
AllPlayingCardsDict["%s-A-%s" % (PlayingCardNames.Appaloosa, PlayingCardSuits.Spade)]         = PlayingCard(PlayingCardNames.Appaloosa, "A", PlayingCardSuits.Spade, PlayingCardColors.Blue)


ADeckOfCards = list(AllPlayingCardsDict.values()) + [AllPlayingCardsDict["%s-9-%s" % (PlayingCardNames.StageCoach, PlayingCardSuits.Spade)]]

if __name__ == "__main__":

    print (len(ADeckOfCards))
    count = 0
    for c in AllPlayingCardsDict.values():
        if c.color == PlayingCardColors.Blue:
            count += 1
    print ("blue", count)
