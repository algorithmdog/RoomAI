#!/bin/python
#coding:utf-8

import logging
import random
from functools import cmp_to_key

import roomai
import roomai.games.common
from roomai.games.texasholdem import *


class TexasHoldemEnv(roomai.games.common.AbstractEnv):
    '''
    The TexasHoldem game environment
    '''


    params=dict()#@override
    def init(self, params = dict()):
        '''
        Initialize the TexasHoldem game environment with the initialization params.\n
        The initialization is a dict with some options\n
    
        1. param_num_normal_players: how many players are in the game, default 3\n
        2. param_dealer_id: the player id of the dealer, default random\n
        3. param_init_chips: the initialization chips, default [1000,1000,...]\n
        4. param_big_blind_bet: the number of chips for the big blind bet, default 10\n
        An example of the initialization param is {"param_num_normal_players":2,"backward_enable":True}
        
        :param params: the initialization params
        :return: infos, public_state, person_states, private_state
        '''

        logger         = roomai.get_logger()
        public_state   = TexasHoldemStatePublic()
        self.__public_state_history__.append(public_state)

        if "param_num_normal_players" in params:
            public_state.__param_num_normal_players__ = params["param_num_normal_players"]
        else:
            public_state.__param_num_normal_players__ = 3

        if "param_dealer_id" in params:
            public_state.__param_dealer_id__ = params["param_dealer_id"]
        else:
            public_state.__param_dealer_id__ = int(random.random() * public_state.param_num_normal_players)

        if "param_init_chips" in params:
            public_state.__param_init_chips__     = params["param_init_chips"]
        else:
            public_state.__param_init_chips__     = [1000 for i in range(public_state.param_num_normal_players)]

        if "param_big_blind_bet" in params:
            public_state.__param_big_blind_bet__ = params["param_big_blind_bet"]
        else:
            public_state.__param_big_blind_bet__ = 10

        ## check initialization config
        if len(public_state.param_init_chips) != public_state.param_num_normal_players:
            raise ValueError("len(env.param_initialization_chips) %d != param_num_normal_players %d" % (len(public_state.param_init_chips), public_state.param_num_normal_players))
        if public_state.param_num_normal_players > 6:
            raise ValueError(
                "The maximum of the number of players is 6. Now, the number of players = %d" % (public_state.param_num_normal_players))



        ## public info
        small = (public_state.param_dealer_id + 1) % public_state.param_num_normal_players
        big   = (public_state.param_dealer_id + 2) % public_state.param_num_normal_players

        pu                           = public_state


        pu.__is_fold__               = [False for i in range(public_state.param_num_normal_players)]
        pu.__num_fold__              = 0
        pu.__is_allin__              = [False for i in range(public_state.param_num_normal_players)]
        pu.__num_allin__             = 0
        pu.__is_needed_to_action__   = [True for i in range(public_state.param_num_normal_players)]
        pu.__num_needed_to_action__  = pu.param_num_normal_players

        pu.__bets__                  = [0 for i in range(public_state.param_num_normal_players)]
        pu.__chips__                 = list(public_state.param_init_chips)
        pu.__stage__                 = Stage.firstStage
        pu.__turn__                  = pu.param_num_normal_players
        pu.__public_cards__          = []

        pu.__previous_id__           = None
        pu.__previous_action__       = None

        if pu.chips[big] > public_state.param_big_blind_bet:
            pu.__chips__[big] -= public_state.param_big_blind_bet
            pu.__bets__[big]  += public_state.param_big_blind_bet
        else:
            pu.__bets__[big]     = pu.chips[big]
            pu.__chips__[big]    = 0
            pu.__is_allin__[big] = True
            pu.__num_allin__    += 1
        pu.__max_bet_sofar__ = pu.bets[big]
        pu.__raise_account__ = public_state.param_big_blind_bet

        if pu.chips[small] > public_state.param_big_blind_bet / 2:
            pu.__chips__[small] -= public_state.param_big_blind_bet /2
            pu.__bets__[small]  += public_state.param_big_blind_bet /2
        else:
            pu.__bets__[small]     = pu.chips[small]
            pu.__chips__[small]    = 0
            pu.__is_allin__[small] = True
            pu.__num_allin__      += 1

        pu.__is_terminal__         = False
        pu.__scores__              = [0 for i in range(public_state.param_num_normal_players)]

        # private info
        pr                     =  TexasHoldemStatePrivate()
        self.__private_state_history__.append(pr)
        pr.__keep_cards__        = []
        ##pr.__keep_cards__      =allcards[public_state.param_num_normal_players*2:public_state.param_num_normal_players*2+5]

        ## person info
        self.__person_states_history__ = [[] for i in range(pu.param_num_normal_players + 1)]
        for i in range(pu.param_num_normal_players + 1):
            self.__person_states_history__[i].append(TexasHoldemStatePerson())
            self.__person_states_history__[i][0].__id__ = i
            self.__person_states_history__[i][0].__hand_cards__ = []

        self.__person_states_history__[pu.turn][0].__available_actions__ = self.available_actions()

        infos = self.__gen_infos__()

        if logger.level <= logging.DEBUG:
            logger.debug("TexasHoldemEnv.init: param_num_normal_players = %d, param_dealer_id = %d, param_initialization_chip = %d, param_big_blind_bet = %d"%(\
                pu.param_num_normal_players,\
                pu.param_dealer_id,\
                pu.param_init_chips[0],\
                pu.param_big_blind_bet
            ))

        return infos, self.__public_state_history__, self.__person_states_history__, self.__private_state_history__, self.__playerid_action_history__

    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        '''
        The TexasHoldem game environments steps with the action taken by the current player
        
        :param action: The action taken by the current player
        :return: infos, public_state, person_states, private_state
        '''

        logger     = roomai.get_logger()
        pu         = self.__public_state_history__[-1].__deepcopy__()
        pes        = [self.__person_states_history__[i][-1].__deepcopy__() for i in range(len(self.__person_states_history__))]
        pr         = self.__private_state_history__[-1].__deepcopy__()

        self.__public_state_history__.append(pu)
        for i in range(len(pes)):
            self.__person_states_history__[i].append(pes[i])
        self.__private_state_history__.append(pr)

        if action.key not in pes[pu.turn].available_actions:
            logger.critical("action=%s is invalid" % (action.key))
            raise ValueError("action=%s is invalid" % (action.key))
        pes[pu.turn].__available_actions__ = dict()
        self.__playerid_action_history__.append(roomai.games.common.ActionRecord(pu.turn,action))

        if isinstance(action, TexasHoldemActionChance) == True:
            self.__action_chance__(action)

            if len(pr.all_used_cards) == (len(pes)-1) * 2 + 5:
                pu.__turn__ = (pu.param_dealer_id + 2 + 1)%pu.param_num_normal_players

            pes[pu.turn].__available_actions__ = self.available_actions()

            infos = self.__gen_infos__()
            return infos, self.__public_state_history__, self.__person_states_history__, self.__private_state_history__, self.__playerid_action_history__

        if action.option == TexasHoldemAction.Fold:
            self.__action_fold__(action)
        elif action.option == TexasHoldemAction.Check:
            self.__action_check__(action)
        elif action.option == TexasHoldemAction.Call:
            self.__action_call__(action)
        elif action.option == TexasHoldemAction.Raise:
            self.__action_raise__(action)
        elif action.option == TexasHoldemAction.AllIn:
            self.__action_allin__(action)
        else:
            raise Exception("action.option(%s) not in [Fold, Check, Call, Raise, AllIn]"%(action.option))
        pu.__previous_id__     = pu.turn
        pu.__previous_action__ = action
        pu.__is_terminal__     = False
        pu.__scores__          = [0 for i in range(self.__public_state_history__[-1].param_num_normal_players)]

        # computing_score
        if TexasHoldemEnv.__is_compute_scores__(self.__public_state_history__[-1]):
            ## need showdown
            pu.__public_cards__ = pr.keep_cards[0:5]
            pu.__is_terminal__  = True
            pu.__scores__       = self.__compute_scores__()


        # enter into the next stage
        elif TexasHoldemEnv.__is_nextround__(self.__public_state_history__[-1]):
            add_cards = []
            if pu.stage == Stage.firstStage:   add_cards = pr.keep_cards[0:3]
            if pu.stage == Stage.secondStage:  add_cards = [pr.keep_cards[3]]
            if pu.stage == Stage.thirdStage:   add_cards = [pr.keep_cards[4]]

            pu.__public_cards__.extend(add_cards)
            pu.__stage__                      = pu.stage + 1

            pu.__num_needed_to_action__       = 0
            pu.__is_needed_to_action__        = [False for i in range(pu.param_num_normal_players)]
            for i in range(pu.param_num_normal_players):
                if pu.__is_fold__[i] != True and pu.__is_allin__[i] != True:
                    pu.__is_needed_to_action__[i]      = True
                    pu.__num_needed_to_action__       += 1

            pu.__turn__                                             = pu.param_dealer_id
            pu.__turn__                                             = self.__next_player__(pu)
            pes[self.__public_state_history__[-1].turn].__available_actions__        = self.available_actions()

        ##normal
        else:
            pu.__turn__  = self.__next_player__(pu)
            self.__person_states_history__[self.__public_state_history__[-1].turn][-1].__available_actions__        = self.available_actions()

        logger = roomai.get_logger()

        if logger.level <= logging.DEBUG:
            logger.debug("TexasHoldemEnv.forward: num_fold+num_allin = %d+%d = %d, action = %s, stage = %d"%(\
                self.__public_state_history__[-1].num_fold,\
                self.__public_state_history__[-1].num_allin,\
                self.__public_state_history__[-1].num_fold + self.__public_state_history__[-1].num_allin,\
                action.key,\
                self.__public_state_history__[-1].stage\
            ))

        infos = self.__gen_infos__()
        return infos, self.__public_state_history__, self.__person_states_history__, self.__private_state_history__, self.__playerid_action_history__

    def available_actions(self):
        '''
        Generate all valid actions given the public state and the person state

        :return: all valid actions
        '''

        pu  = self.__public_state_history__[-1]
        pes = [self.__person_states_history__[i][-1] for i in range(len(self.__person_states_history__))]
        pr  = self.__private_state_history__[-1]

        if len(pr.all_used_cards) < (len(pes)-1) * 2 + 5:
            candidate_chance_actions = dict()
            all_used_card_keys = set([c.key for c in pr.all_used_cards])
            for card_key in AllPokerCardsDict:
                if card_key not in all_used_card_keys:
                    chance_action = TexasHoldemActionChance.lookup(card_key)
                    candidate_chance_actions[chance_action.key] = chance_action
            return candidate_chance_actions

        pe = pes[pu.turn]
        turn = pu.turn
        key_actions = dict()

        if pu.turn != pe.id:
            return dict()

        if pu.is_allin[turn] == True or pu.is_fold[turn] == True:
            return dict()
        if pu.chips[turn] == 0:
            return dict()

        ## for fold
        action = TexasHoldemAction.lookup(TexasHoldemAction.Fold + "_0")
        # if cls.is_action_valid(action,public_state, person_state):
        key_actions[action.key] = action

        ## for check
        if pu.bets[turn] == pu.max_bet_sofar:
            action = TexasHoldemAction.lookup(TexasHoldemAction.Check + "_0")
            # if cls.is_action_valid(action, public_state, person_state):
            key_actions[action.key] = action

        ## for call
        if pu.bets[turn] != pu.max_bet_sofar and pu.chips[turn] > pu.max_bet_sofar - pu.bets[turn]:
            action = TexasHoldemAction.lookup(TexasHoldemAction.Call + "_%d" % (pu.max_bet_sofar - pu.bets[turn]))
            # if cls.is_action_valid(action, public_state, person_state):
            key_actions[action.key] = action

        ## for raise
        # if pu.bets[turn] != pu.max_bet_sofar and \
        if pu.chips[turn] > pu.max_bet_sofar - pu.bets[turn] + pu.raise_account:
            num = int((pu.chips[turn] - (pu.max_bet_sofar - pu.bets[turn])) / pu.raise_account)
            for i in range(1, num + 1):
                price = pu.max_bet_sofar - pu.bets[turn] + pu.raise_account * i
                if price == pu.chips[pu.turn]:  continue
                action = TexasHoldemAction.lookup(TexasHoldemAction.Raise + "_%d" % (price))
                # if cls.is_action_valid(action, public_state, person_state):
                key_actions[action.key] = action

        ## for all in
        action = TexasHoldemAction.lookup(TexasHoldemAction.AllIn + "_%d" % (pu.chips[turn]))
        # if cls.is_action_valid(action, public_state, person_state):
        key_actions[action.key] = action

        return key_actions

    def __compute_scores__(self):
        pu  = self.__public_state_history__[-1]
        pes = [self.__person_states_history__[i][-1] for i in range(len(self.__person_states_history__))]
        pr  = self.__private_state_history__[-1]

        ## compute score before showdown, the winner takes all
        if pu.param_num_normal_players  ==  pu.num_fold + 1:
            scores = [0 for i in range(pu.param_num_normal_players)]
            for i in range(pu.param_num_normal_players):
                if pu.is_fold[i] == False:
                    scores[i] = sum(pu.bets)
                    break

        ## compute score after showdown
        else:
            scores                = [0 for i in range(pu.param_num_normal_players)]
            playerid_pattern_bets = [] #for not_quit players
            for i in range(pu.param_num_normal_players):
                if pu.is_fold[i] == True: continue
                hand_pattern_cards = self.__cards2pattern_cards__(pes[i].hand_cards, pr.keep_cards)
                playerid_pattern_bets.append((i,hand_pattern_cards,pu.bets[i]))

            for playerid_pattern_bet in playerid_pattern_bets:
                if len(playerid_pattern_bet[1][1]) < 5:
                    i = 0

            playerid_pattern_bets.sort(key=lambda x:self.compute_rank_pattern_cards(x[1]))

            pot_line = 0
            previous = None
            tmp_playerid_pattern_bets      = []
            for i in range(len(playerid_pattern_bets)-1,-1,-1):
                if previous == None:
                    tmp_playerid_pattern_bets.append(playerid_pattern_bets[i])
                    previous = playerid_pattern_bets[i]
                elif self.__compare_patterns_cards__(playerid_pattern_bets[i][1], previous[1]) == 0:
                    tmp_playerid_pattern_bets.append(playerid_pattern_bets[i])
                    previous = playerid_pattern_bets[i]
                else:
                    tmp_playerid_pattern_bets.sort(key = lambda x:x[2])
                    for k in range(len(tmp_playerid_pattern_bets)):
                        num1          = len(tmp_playerid_pattern_bets) - k
                        sum1          = 0
                        max_win_score = pu.bets[tmp_playerid_pattern_bets[k][0]]
                        for p in range(pu.param_num_normal_players):
                            sum1      += min(max(0, pu.bets[p] - pot_line), max_win_score)
                        for p in range(k, len(tmp_playerid_pattern_bets)):
                            scores[tmp_playerid_pattern_bets[p][0]] += sum1 / num1
                        scores[pu.param_dealer_id] += sum1 % num1
                        if pot_line <= max_win_score:
                            pot_line = max_win_score
                    tmp_playerid_pattern_bets = []
                    tmp_playerid_pattern_bets.append(playerid_pattern_bets[i])
                    previous = playerid_pattern_bets[i]


            if len(tmp_playerid_pattern_bets) > 0:
                tmp_playerid_pattern_bets.sort(key = lambda  x:x[2])
                for i in range(len(tmp_playerid_pattern_bets)):
                    num1 = len(tmp_playerid_pattern_bets) - i
                    sum1 = 0
                    max_win_score = pu.bets[tmp_playerid_pattern_bets[i][0]]
                    for p in range(pu.param_num_normal_players):
                        sum1 += min(max(0, pu.bets[p] - pot_line), max_win_score)
                    for p in range(i, len(tmp_playerid_pattern_bets)):
                        scores[tmp_playerid_pattern_bets[p][0]] += sum1 / num1
                    scores[pu.param_dealer_id] += sum1 % num1
                    if pot_line <= max_win_score: pot_line = max_win_score

        for p in range(pu.param_num_normal_players):
            pu.__chips__[p] += scores[p]
            scores[p]   -= pu.bets[p]

        for p in range(pu.param_num_normal_players):
            scores[p]   /= pu.param_big_blind_bet * 1.0
        return scores

    def __action_chance__(self, action):
        pu = self.__public_state_history__[-1]
        pes = [self.__person_states_history__[i][-1] for i in range(len(self.__person_states_history__))]
        pr = self.__private_state_history__[-1]


        card = action.card
        num  = len(pr.all_used_cards)
        if num < (len(pes)-1) * 2:
            idx = int(num / 2)
            pes[idx].__hand_cards__.append(card)

        elif num < (len(pes)-1) * 2 + 5:
            pr.__keep_cards__.append(card)

        else:
            logger = roomai.get_logger()
            logger.fatal("the chance action in the invalid condition")

        pr.__all_used_cards__.append(card)


    def __action_fold__(self, action):
        pu = self.__public_state_history__[-1]
        pu.__is_fold__[pu.turn]             = True
        pu.__num_fold__                    += 1

        pu.__is_needed_to_action__[pu.turn] = False
        pu.__num_needed_to_action__        -= 1

    def __action_check__(self, action):
        pu = self.__public_state_history__[-1]
        pu.__is_needed_to_action__[pu.turn] = False
        pu.__num_needed_to_action__        -= 1

    def __action_call__(self, action):
        pu = self.__public_state_history__[-1]
        pu.__chips__[pu.turn] -= action.price
        pu.__bets__[pu.turn]  += action.price
        pu.__is_needed_to_action__[pu.turn] = False
        pu.__num_needed_to_action__        -= 1

    def __action_raise__(self, action):
        pu = self.__public_state_history__[-1]

        pu.__raise_account__   = action.price + pu.bets[pu.turn] - pu.max_bet_sofar
        pu.__chips__[pu.turn] -= action.price
        pu.__bets__[pu.turn]  += action.price
        pu.__max_bet_sofar__   = pu.bets[pu.turn]

        pu.__is_needed_to_action__[pu.turn] = False
        pu.__num_needed_to_action__        -= 1
        p = (pu.turn + 1)%pu.param_num_normal_players
        while p != pu.turn:
            if pu.is_allin[p] == False and pu.is_fold[p] == False and pu.is_needed_to_action[p] == False:
                pu.__num_needed_to_action__   += 1
                pu.__is_needed_to_action__[p]  = True
            p = (p + 1) % pu.param_num_normal_players


    def __action_allin__(self, action):
        pu = self.__public_state_history__[-1]

        pu.__is_allin__[pu.turn]   = True
        pu.__num_allin__          += 1

        pu.__bets__[pu.turn]      += action.price
        pu.__chips__[pu.turn]      = 0

        pu.__is_needed_to_action__[pu.turn] = False
        pu.__num_needed_to_action__        -= 1
        if pu.bets[pu.turn] > pu.max_bet_sofar:
            pu.__max_bet_sofar__ = pu.bets[pu.turn]
            p = (pu.turn + 1) % pu.param_num_normal_players
            while p != pu.turn:
                if pu.is_allin[p] == False and pu.is_fold[p] == False and pu.is_needed_to_action[p] == False:
                    pu.__num_needed_to_action__  += 1
                    pu.__is_needed_to_action__[p] = True
                p = (p + 1) % pu.param_num_normal_players

            pu.__max_bet_sofar__ = pu.bets[pu.turn]



#####################################Utils Function ##############################
        # override

    @classmethod
    def compete_silent(cls, env, players):
        '''
        Use the game environment to hold a compete_silent for the players

        :param env: The game environment
        :param players: The normal players (without the chance player)
        :return: scores for the players
        '''

        total_scores = [0 for i in range(len(players))]
        total_count = 10
        num_normal_players = len(players)

        players = players + [roomai.games.common.RandomPlayerChance()]

        for count in range(total_count):

            chips = [(1000 + int(random.random() * 200)) for i in range(len(players))]
            dealer_id = int(random.random() * len(players))
            big_blind_bet = 50

            infos, public, persons, private, action_history = env.init({"chips": chips,
                                                        "param_num_normal_players": num_normal_players,
                                                        "dealer_id": dealer_id,
                                                        "big_blind_bet": big_blind_bet})
            for i in range(len(players)):
                players[i].receive_info(infos[i])
            while public[-1].is_terminal == False:
                turn = public[-1].turn
                action = players[turn].take_action()
                # print len(infos[turn].person_state.available_actions),action.key(),turn
                infos, public, persons, private, _= env.forward(action)
                for i in range(len(players)):
                    players[i].receive_info(infos[i])

            for i in range(len(players)):
                players[i].receive_info(infos[i])
            for i in range(num_normal_players):
                total_scores[i] += public[-1].scores[i]

            if (count + 1) % 500 == 0:
                tmp_scores = [0 for i in range(len(total_scores))]
                for i in range(len(total_scores)):
                    tmp_scores[i] = total_scores[i] / (count + 1)
                roomai.get_logger().info("TexasHoldem completes %d competitions, scores=%s" % (
                count + 1, ",".join([str(i) for i in tmp_scores])))

        for i in range(len(total_scores)):
            total_scores[i] /= 1.0 * total_count

        return total_scores

    @classmethod
    def __next_player__(self, pu):
        i = pu.turn
        if pu.num_needed_to_action == 0:
            return -1

        p = (i+1)%pu.param_num_normal_players
        while pu.is_needed_to_action[p] == False:
            p = (p+1)%pu.param_num_normal_players
        return p

    @classmethod
    def __is_compute_scores__(self, pu):
        '''
        :return: A boolean variable indicates whether is it time to compute scores
        '''

        if pu.param_num_normal_players == pu.num_fold + 1:
            return True

        # below need showdown

        if pu.param_num_normal_players <=  pu.num_fold + pu.num_allin +1 and pu.num_needed_to_action == 0:
            return True

        if pu.stage == Stage.fourthStage and self.__is_nextround__(pu):
            return True

        return False

    @classmethod
    def __is_nextround__(self, public_state):
        '''
        :return: A boolean variable indicates whether is it time to enter the next stage
        '''
        return public_state.num_needed_to_action == 0

    @classmethod
    def __cards2pattern_cards__(cls, hand_cards, remaining_cards):
        key = cmp_to_key(roomai.games.texasholdem.PokerCard.compare)
        pointrank2cards = dict()
        for c in hand_cards + remaining_cards:
            if c.point_rank in pointrank2cards:
                pointrank2cards[c.point_rank].append(c)
            else:
                pointrank2cards[c.point_rank] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(key = key)

        suitrank2cards = dict()
        for c in hand_cards + remaining_cards:
            if c.suit_rank in suitrank2cards:
                suitrank2cards[c.suit_rank].append(c)
            else:
                suitrank2cards[c.suit_rank] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(key=key)

        num2point = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2point[num].append(p)
        for i in range(5):
            num2point[num].sort()

        sorted_point = []
        for p in pointrank2cards:
            sorted_point.append(p)
        sorted_point.sort()

        ##straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                numStraight = 1
                for i in range(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].point_rank == suitrank2cards[s][i + 1].point_rank - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = AllCardsPattern["Straight_SameSuit"]
                        return (pattern,suitrank2cards[s][i:i + 5])

        ##4_1
        if len(num2point[4]) > 0:
            p4 = num2point[4][0]
            p1 = -1
            for i in range(len(sorted_point) - 1, -1, -1):
                if sorted_point[i] != p4:
                    p1 = sorted_point[i]
                    break
            pattern = AllCardsPattern["4_1"]
            cards   = pointrank2cards[p4][0:4]
            cards.append(pointrank2cards[p1][0])

            return (pattern,cards)

        ##3_2
        if len(num2point[3]) >= 1:
            pattern = AllCardsPattern["3_2"]

            if len(num2point[3]) == 2:
                p3 = num2point[3][1]
                cards = pointrank2cards[p3][0:3]
                p2 = num2point[3][0]
                cards.append(pointrank2cards[p2][0])
                cards.append(pointrank2cards[p2][1])
                return (pattern,cards)

            if len(num2point[2]) >= 1:
                p3 = num2point[3][0]
                cards = pointrank2cards[p3][0:3]
                p2 = num2point[2][len(num2point[2]) - 1]
                cards.append(pointrank2cards[p2][0])
                cards.append(pointrank2cards[p2][1])
                return (pattern,cards)

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                pattern = AllCardsPattern["SameSuit"]
                len1 = len(suitrank2cards[s])
                cards = suitrank2cards[s][len1 - 5:len1]
                return (pattern,cards)

        ##Straight_DiffSuit
        numStraight = 1
        for idx in range(len(sorted_point) - 2, -1, -1):
            if sorted_point[idx] + 1 == sorted_point[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern = AllCardsPattern["Straight_DiffSuit"]
                cards = []
                for p in range(idx, idx + 5):
                    point = sorted_point[p]
                    cards.append(pointrank2cards[point][0])
                return (pattern,cards)

        ##3_1_1
        if len(num2point[3]) == 1:
            pattern = AllCardsPattern["3_1_1"]

            p3 = num2point[3][0]
            cards = pointrank2cards[p3][0:3]

            num = 0
            for i in range(len(sorted_point) - 1, -1, -1):
                p = sorted_point[i]
                if p != p3:
                    cards.append(pointrank2cards[p][0])
                    num += 1
                if num == 2:    break
            return (pattern,cards)

        ##2_2_1
        if len(num2point[2]) >= 2:
            pattern = AllCardsPattern["2_2_1"]
            p21 = num2point[2][len(num2point[2]) - 1]
            cards = []
            for c in pointrank2cards[p21]:
                cards.append(c)
            p22 = num2point[2][len(num2point[2]) - 2]
            for c in pointrank2cards[p22]:
                cards.append(c)

            flag = False
            for i in range(len(sorted_point) - 1, -1, -1):
                p = sorted_point[i]
                if p != p21 and p != p22:
                    c = pointrank2cards[p][0]
                    cards.append(c)
                    flag = True
                if flag == True:    break;
            return (pattern,cards)

        ##2_1_1_1
        if len(num2point[2]) == 1:
            pattern = AllCardsPattern["2_1_1_1"]
            p2 = num2point[2][0]
            cards = pointrank2cards[p2][0:2]
            num = 0
            for p in range(len(sorted_point) - 1, -1, -1):
                p1 = sorted_point[p]
                if p1 != p2:
                    cards.append(pointrank2cards[p1][0])
                if num == 3:    break
            return (pattern,cards)

        ##1_1_1_1_1
        pattern = AllCardsPattern["1_1_1_1_1"]
        count = 0
        cards = []
        for i in range(len(sorted_point) - 1, -1, -1):
            p = sorted_point[i]
            for c in pointrank2cards[p]:
                cards.append(c)
                count += 1
                if count == 5: break
            if count == 5: break
        return (pattern,cards)

    @classmethod
    def __compare_handcards__(cls, hand_card0, hand_card1, keep_cards):
        pattern0 = TexasHoldemEnv.__cards2pattern_cards__(hand_card0, keep_cards)
        pattern1 = TexasHoldemEnv.__cards2pattern_cards__(hand_card1, keep_cards)

        diff = cls.__compare_patterns_cards__(pattern0, pattern1)
        return diff

    @classmethod
    def compute_rank_pattern_cards(cls, pattern_cards):
        rank = pattern_cards[0][5] * 1000
        for i in range(5):
            rank *= 1000
            rank += pattern_cards[1][i].point_rank
        return rank

    @classmethod
    def __compare_patterns_cards__(cls, p1, p2):
        return cls.compute_rank_pattern_cards(p1) - cls.compute_rank_pattern_cards(p2)


    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = TexasHoldemEnv()
        newinstance = super(TexasHoldemEnv, self).__deepcopy__(newinstance=newinstance)
        return newinstance
