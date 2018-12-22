#!/bin/python
#coding:utf-8

import roomai

class Stage:
    firstStage  = 1
    secondStage = 2
    thirdStage  = 3
    fourthStage = 4


AllCardsPattern = dict()
#0     1           2       3           4                                    5     6
#name, isStraight, isPair, isSameSuit, [SizeOfPair1, SizeOfPair2,..](desc), rank, cards
AllCardsPattern["Straight_SameSuit"] = \
["Straight_SameSuit",   True,  False, True,  [],         100]
AllCardsPattern["4_1"] = \
["4_1",                 False, True,  False, [4,1],      98]
AllCardsPattern["3_2"] = \
["3_2",                 False, True,  False, [3,2],      97]
AllCardsPattern["SameSuit"] = \
["SameSuit",            False, False, True,  [],         96]
AllCardsPattern["Straight_DiffSuit"] = \
["Straight_DiffSuit",   True,  False, False, [],         95]
AllCardsPattern["3_1_1"] = \
["3_1_1",               False, True,  False, [3,1,1],    94]
AllCardsPattern["2_2_1"] = \
["2_2_1",               False, True,  False, [2,2,1],    93]
AllCardsPattern["2_1_1_1"] = \
["2_1_1_1",             False, True,  False, [2,1,1,1],  92]
AllCardsPattern["1_1_1_1_1"] = \
["1_1_1_1_1",           False, True,  False, [1,1,1,1,1],91]

point_str_to_rank = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
point_rank_to_str = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
suit_str_to_rank = {'Spade': 0, 'Heart': 1, 'Diamond': 2, 'Club': 3}
suit_rank_to_str = {0: 'Spade', 1: 'Heart', 2: 'Diamond', 3: 'Club'}


class PokerCard(object):
    '''
    A Poker Card. \n
    A Poker Card has a point (2,3,4,....,K,A) and a suit (Spade, Heart, Diamond, Club). \n
    Different points have different ranks, for example the point 2's rank is 0, and the point A's rank is 12. \n
    Different suits have different ranks too. \n
    A Poker Card has a key (point_suit). We strongly recommend you to get a poker normalcard by using the class function lookup with the key. \n
    Examples of the class usages: \n
    >> import roomai.games.texasholdem \n
    >> normalcard = roomai.games.texasholdem.Card.lookup("2-Spade") \n
    >> normalcard.point \n
    2\n
    >> normalcard.suit\n
    Spade\n
    >> normalcard.point_rank\n
    0\n
    >> normalcard.suit_rank\n
    0\n
    >> normalcard.key\n
    "2-Spade"\n
    '''

    def __init__(self, point, suit=None):
        point1 = 0
        suit1 = 0
        if suit is None:
            kv = point.split("-")
            point1 = point_str_to_rank[kv[0]]
            suit1 = suit_str_to_rank[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_rank[point]
            suit1 = suit
            if isinstance(suit, str):
                suit1 = suit_str_to_rank[suit]

        self.__point__ = point_rank_to_str[point1]
        self.__suit__ = suit_rank_to_str[suit1]
        self.__point_rank__ = point1
        self.__suit_rank__ = suit1
        self.__key__ = "%s-%s" % (self.__point__, self.__suit__)

    def __get_point_str__(self):
        return self.__point__
    point = property(__get_point_str__, doc="The point of the poker normalcard")

    def __get_suit_str__(self):
        return self.__suit__
    suit = property(__get_suit_str__, doc="The suit of the poker normalcard")

    def __get_point_rank__(self):
        return self.__point_rank__
    point_rank = property(__get_point_rank__, doc="The point rank of the poker normalcard")

    def __get_suit_rank__(self):
        return self.__suit_rank__
    suit_rank = property(__get_suit_rank__, doc="The suit rank of the poker normalcard")

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the poker normalcard")

    @classmethod
    def lookup(cls, key):
        '''
        lookup a Card with the specified key

        :param key: The specified key
        :return: The Card with the specified key
        '''

        logger = roomai.get_logger()
        if key not in AllPokerCardsDict:
            logger.fatal("key (%s) is not invalid poker normalcard key"%(key))
            raise ValueError("key (%s) is not invalid poker normalcard key"%(key))

        return AllPokerCardsDict[key]

    @classmethod
    def point_to_rank(cls, point):
        if point not in point_str_to_rank:
            raise ValueError("%s is invalid poker point for Card")
        return point_str_to_rank[point]

    @classmethod
    def suit_to_rank(cls, suit):
        if suit not in suit_str_to_rank:
            raise ValueError("%s is invalid poker suit for Card")
        return suit_str_to_rank[suit]

    @classmethod
    def rank_to_point(cls, rank):
        if rank not in point_rank_to_str:
            raise ValueError("%d is invalid poker point rank for Card")
        return point_rank_to_str[rank]

    @classmethod
    def rank_to_suit(cls, rank):
        if rank not in suit_rank_to_str:
            raise ValueError("%d is invalid poker suit rank for Card")
        return suit_rank_to_str[rank]

    @classmethod
    def compare(cls, pokercard1, pokercard2):
        '''
        Compare two poker cards with their point ranks and suit ranks.
        The poker normalcard with the higher point rank has the higher rank.
        With the same point rank, the poker normalcard with the higher suit rank has the higher rank.

        :param pokercard1: 
        :param pokercard2: 
        :return: A number, which is >0 when the poker card1 has the higher rank than the poker card2, =0 when their share the same rank, <0 when the poker card1 has the lower rank than the poker card2

        '''
        pr1 = pokercard1.point_rank
        pr2 = pokercard2.point_rank

        if pr1 != pr2:
            return pr1 - pr2
        else:
            return pokercard1.suit_rank - pokercard2.suit_rank

    def __deepcopy__(self, memodict={}, newinstance=None):
        return AllPokerCardsDict[self.key]


AllPokerCardsDict = dict()
for point in point_str_to_rank:
    for suit in suit_str_to_rank:
        AllPokerCardsDict["%s-%s" % (point, suit)] = PokerCard("%s-%s" % (point, suit))







