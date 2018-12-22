#!/bin/python
#coding:utf-8
import roomai.games.common


class TexasHoldemStatePublic(roomai.games.common.AbstractStatePublic):
    '''
    The public state of TexasHoldem
    '''
    def __init__(self):
        super(TexasHoldemStatePublic, self).__init__()
        self.__stage__              = None
        self.__public_cards__       = None

        #state of players
        self.__is_fold__                        = None
        self.__num_fold__                       = None
        self.__is_allin__                       = None
        self.__num_allin__                      = None
        self.__is_needed_to_action__            = None
        self.__num_needed_to_action__           = None

        self.__param_dealer_id__ = -1
        self.__param_big_blind_bet__ = -1
        self.__param_init_chips__ = None


        #chips is array which contains the chips of all players
        self.__chips__              = None

        #bets is array which contains the bets from all players
        self.__bets__               = None

        #max_bet = max(self.bets)
        self.__max_bet_sofar__      = None
        #the raise acount
        self.__raise_account__      = None


    def __get_max_bet_sofar__(self):    return self.__max_bet_sofar__
    max_bet_sofar = property(__get_max_bet_sofar__, doc="The max bet used by one player so far")

    def __get_raise_account__(self):   return self.__raise_account__
    raise_account = property(__get_raise_account__, doc="The raise account. If a player want to raise, the price must be max_bet_sofar + raise_account * N. The raise account will increases as the game goes forward")

    def __get_chips__(self):
        if self.__chips__ is None:
            return None
        else:
            return tuple(self.__chips__)
    chips = property(__get_chips__, doc = "chips is an array of the chips of all players. For example, chips=[50,50,50]")

    def __get_bets__(self):
        if self.__bets__ is None:
            return None
        else:
            return tuple(self.__bets__)
    bets = property(__get_bets__, doc = "bets is an array which contains the bets from all players. For example, bets=[50,25,25]")



    def __get_is_fold__(self):
        if self.__is_fold__ is None:    return None
        else:   return tuple(self.__is_fold__)
    is_fold = property(__get_is_fold__, doc="is_fold is an array of which player has take the fold action. For example, is_fold = [true,true,false] denotes the player0 and player1 have taken the fold action")

    def __get_num_fold__(self):
        return self.__num_fold__
    num_fold = property(__get_num_fold__, doc = "The number of players who has taken the fold action")

    def __get_is_allin__(self):
        if self.__is_allin__ is None:    return None
        else:   return tuple(self.__is_allin__)
    is_allin = property(__get_is_allin__, doc="is_allin is an array of which player has take the allin action. For example, is_allin = [true,true,false] denotes the player0 and player1 have taken the allin action")

    def __get_num_allin__(self):
        return self.__num_allin__
    num_allin = property(__get_num_allin__, doc = "The number of players who has taken the allin action")


    def __get_is_needed_to_action__(self):
        if self.__is_needed_to_action__ is None:    return None
        else:   return tuple(self.__is_needed_to_action__)
    is_needed_to_action = property(__get_is_needed_to_action__, doc="is_needed_to_action is an array of which player has take the needed_to_action action. For example, is_needed_to_action = [true,true,false] denotes the player0 and player1 are need to take action")

    def __get_num_needed_to_action__(self):
        return self.__num_needed_to_action__
    num_needed_to_action = property(__get_num_needed_to_action__, doc = "The number of players who has taken the needed_to_action action")

    def __get_public_cards__(self):
        if self.__public_cards__ is None:
            return None
        else:
            return tuple(self.__public_cards__)
    public_cards = property(__get_public_cards__, doc="The public cards of this game. For example, public_cards = [roomai.common.PokerCards.lookup(\"A_Spade\"), roomai.common.PokerCards.lookup(\"A_Heart\")]")

    def __get_stage__(self):
        return self.__stage__
    stage = property(__get_stage__, doc="The stage of the TexasHoldem game. The stage must be one of 1,2,3 or 4.")



    ######################### initialization param ##################
    __param_dealer_id__ = 0
    def __get_param_dealer_id__(self):    return self.__param_dealer_id__
    param_dealer_id = property(__get_param_dealer_id__, doc="The player id of the dealer. The next player after the dealer is the small blind. The next player after the small blind is the big blind.For example, param_dealer_id = 2")

    __param_init_chips__ = None
    def __get_param_init_chips__(self):   return self.__param_init_chips__
    param_init_chips = property(__get_param_init_chips__, doc="The initialization chips of this game. For example, param_initialization_chips = [10,5,6]")

    __param_big_blind_bet__ = 10
    def __get_param_big_blind_bet__(self): return self.__param_big_blind_bet__
    param_big_blind_bet = property(__get_param_big_blind_bet__, doc="The big blind bet")


    def __deepcopy__(self, memodict={}, newinstance = None):
            if newinstance is None:
                newinstance = TexasHoldemStatePublic()
            newinstance = super(TexasHoldemStatePublic, self).__deepcopy__(newinstance=newinstance)


            newinstance.__param_dealer_id__     = self.param_dealer_id
            newinstance.__param_big_blind_bet__ = self.param_big_blind_bet
            newinstance.__param_init_chips__    = self.__param_init_chips__


            newinstance.__stage__         = self.stage
            if self.public_cards is None:
                newinstance.__public_cards__ = None
            else:
                newinstance.__public_cards__ = [self.public_cards[i].__deepcopy__() for i in range(len(self.public_cards))]

            ######## quit, allin , needed_to_action
            newinstance.__num_fold__ = self.__num_fold__
            if self.is_fold is None:
                newinstance.__is_fold__ = None
            else:
                newinstance.__is_fold__ = [self.is_fold[i] for i in range(len(self.is_fold))]

            newinstance.__num_allin__ = self.__num_allin__
            if self.is_allin is None:
                newinstance.__is_allin__ = None
            else:
                newinstance.__is_allin__ = [self.is_allin[i] for i in range(len(self.is_allin))]

            newinstance.__num_needed_to_action__     = self.__num_needed_to_action__
            if self.is_needed_to_action is None:
                newinstance.__is_needed_to_action__ = None
            else:
                newinstance.__is_needed_to_action__ = [self.is_needed_to_action[i] for i in
                                                    range(len(self.is_needed_to_action))]

            # chips is array which contains the chips of all players
            if self.chips is None:
                newinstance.__chips__ = None
            else:
                newinstance.__chips__ = [self.chips[i] for i in range(len(self.chips))]

            # bets is array which contains the bets from all players
            if self.bets is None:
                newinstance.__bets__ = None
            else:
                newinstance.__bets__ = [self.bets[i] for i in range(len(self.bets))]

            newinstance.__max_bet_sofar__ = self.max_bet_sofar
            newinstance.__raise_account__ = self.raise_account
            newinstance.__turn__ = self.turn

            ### isterminal, scores
            newinstance.__is_terminal__ = self.is_terminal
            if self.scores is None:
                newinstance.__scores__ = None
            else:
                newinstance.__scores__ = [self.scores[i] for i in range(len(self.scores))]

            return newinstance