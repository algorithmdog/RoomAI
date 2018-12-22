#!/bin/python
import random
import unittest
import roomai
from roomai.games.texasholdem import *
from roomai.games.common import RandomPlayer


class TexasEnvTester(unittest.TestCase):

    def test_continuous_check(self):
        env = roomai.games.texasholdem.TexasHoldemEnv()
        infos, public_history, persons_history, private_history, action_history = env.init({"num_normal_players":3, "big_blind_bet":10})

        pu = public_history[-1]
        pr = private_history[-1]
        pe = persons_history[pu.turn][-1]

        while len(pr.all_used_cards) < (len(persons_history) - 1) * 2 + 5:
            action = list(pe.available_actions.values())[-1]
            env.forward(action)

            pu = public_history[-1]
            pr = private_history[-1]
            pe = persons_history[pu.turn][-1]

        env.forward(TexasHoldemAction.lookup("Call_10"))
        env.forward(TexasHoldemAction.lookup("Call_5"))


    def testEnv3players(self):

        env = TexasHoldemEnv()
        num_normal_players   = 3

        dealer_id     = 0
        chips         = [100,100,100]
        big_blind_bet = 20
        params  = {"param_num_normal_players":num_normal_players, "param_dealer_id":dealer_id, "param_init_chips":chips, "param_big_blind_bet":big_blind_bet, "backward_enable":True}
        players =  [RandomPlayer() for i in range(4)]


        infos,public_state, person_states, private_state,_  = env.init(params)

        for i in range(3*2+5):
            action = list(env.available_actions().values())[0]
            infos, public_state_history, person_states_history, private_state_history, action_history = env.forward(
                action)
            print (i)


        self.assertEqual(infos[0].person_state_history[-1].id,0)
        env.__person_states_history__[0][-1].__hand_cards__ = [roomai.games.texasholdem.PokerCard(0, 0), roomai.games.texasholdem.PokerCard(0, 1)]
        env.__person_states_history__[0][-1].__hand_cards__ = [roomai.games.texasholdem.PokerCard(2, 0), roomai.games.texasholdem.PokerCard(2, 1)]
        env.__person_states_history__[0][-1].__hand_cards__ = [roomai.games.texasholdem.PokerCard(2, 0), roomai.games.texasholdem.PokerCard(2, 1)]
        env.__private_state_history__[-1].__keep_cards__    = [roomai.games.texasholdem.PokerCard(3, 0), roomai.games.texasholdem.PokerCard(4, 0),
                                               roomai.games.texasholdem.PokerCard(5, 0), roomai.games.texasholdem.PokerCard(6, 0),
                                               roomai.games.texasholdem.PokerCard(7, 0)]

        self.assertEqual(env.__public_state_history__[-1].turn, 0)
        self.assertNotEqual(len(infos[0].person_state_history[-1].available_actions), 0)
        self.assertTrue("Allin_100" in infos[0].person_state_history[-1].available_actions.keys())
        # dealer_id = 0
        # turn = 0
        # chips:100, 90, 80
        # bets :0,   10,  20
        # state:n,   n,  n


        action = TexasHoldemAction("Allin_100")
        infos,public_state, person_states, private_state, action_history  = env.forward(action)
        self.assertEqual(env.__public_state_history__[-1].turn, 1)
        self.assertNotEqual(len(infos[1].person_state_history[-1].available_actions), 0)
        self.assertTrue("Allin_90" in infos[1].person_state_history[-1].available_actions.keys())
        self.assertEqual(env.__public_state_history__[-1].turn, 1)
        self.assertEqual(env.__public_state_history__[-1].chips[0],0)
        self.assertEqual(env.__public_state_history__[-1].chips[1],90)
        self.assertEqual(env.__public_state_history__[-1].stage, Stage.firstStage)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  n,  n


        action = TexasHoldemAction("Fold_0")
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        # dealer_id = 0
        # turn = 2
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        self.assertEqual(env.__public_state_history__[-1].turn, 2)


        action = TexasHoldemAction("Fold_0")
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        print (env.__public_state_history__[-1].bets)
        print (env.__public_state_history__[-1].is_allin)
        print (env.__public_state_history__[-1].is_fold)
        print (env.__public_state_history__[-1].chips)
        print (env.__public_state_history__[-1].turn)
        self.assertTrue(public_state[-1].is_terminal)

        self.assertEqual(public_state[-1].scores[0], 30.0/public_state[-1].param_big_blind_bet)
        self.assertEqual(public_state[-1].scores[1], -10.0/public_state[-1].param_big_blind_bet)
        self.assertEqual(public_state[-1].scores[2], -20.0/public_state[-1].param_big_blind_bet)


    def testEnv3Players2(self):
        """

        """

        env = TexasHoldemEnv()
        num_normal_players   = 3
        dealer_id     = 0
        chips         = [100, 500,1000]
        big_blind_bet = 20
        params  = {"param_num_normal_players":num_normal_players, "param_dealer_id":dealer_id, "param_init_chips":chips, "param_big_blind_bet":big_blind_bet}
        players =  [RandomPlayer() for i in range(4)]


        infos,public_state_history, person_states_history, private_state_history, action_history = env.init(params)

        for i in range(3 * 2 + 5):
            action = list(env.available_actions().values())[0]
            infos, public_state_history, person_states_history, private_state_history, action_history = env.forward(action)



        self.assertEqual(infos[0].person_state_history[-1].id,0)
        env.__person_states_history__[0][-1].__hand_cards__ = [roomai.games.texasholdem.PokerCard(7, 0), roomai.games.texasholdem.PokerCard(7, 1)]
        env.__person_states_history__[1][-1].__hand_cards__ = [roomai.games.texasholdem.PokerCard(2, 0), roomai.games.texasholdem.PokerCard(2, 1)]
        env.__person_states_history__[2][-1].__hand_cards__ = [roomai.games.texasholdem.PokerCard(2, 2), roomai.games.texasholdem.PokerCard(2, 3)]
        env.__private_state_history__[-1].__keep_cards__    = [roomai.games.texasholdem.PokerCard(3, 1), roomai.games.texasholdem.PokerCard(4, 2),
                                               roomai.games.texasholdem.PokerCard(5, 3), roomai.games.texasholdem.PokerCard(6, 0),
                                               roomai.games.texasholdem.PokerCard(7, 3)]
        self.assertEqual(env.__public_state_history__[-1].turn, 0)
        self.assertNotEqual(len(infos[0].person_state_history[-1].available_actions), 0)
        self.assertTrue("Raise_60" in infos[0].person_state_history[-1].available_actions.keys())
        self.assertEqual(env.__public_state_history__[-1].raise_account, 20)
        # dealer_id = 0
        # turn = 0
        # chips:100, 490, 980
        # bets :0,   10,  20
        # state:n,   n,  n
        # flag_next:0
        # raise_account: 20


        action = TexasHoldemAction("Raise_60")
        infos,public_state, person_states, private_state, action_history  = env.forward(action)
        print (env.__public_state_history__[-1].num_needed_to_action, env.__public_state_history__[-1].is_needed_to_action)
        self.assertEqual(env.__public_state_history__[-1].turn, 1)
        self.assertTrue("Raise_60" not in infos[1].person_state_history[-1].available_actions)
        self.assertTrue("Raise_80" not in infos[1].person_state_history[-1].available_actions)
        self.assertEqual(env.__public_state_history__[-1].raise_account, 40)
        action = TexasHoldemAction("Call_40")
        self.assertRaises(ValueError, env.forward, action)
        # dealer_id = 0
        # turn  = 1
        # stage = 1
        # chips:40,   490, 980
        # bets :60,   10,  20
        # state:n,   n,  n
        # raise_account: 40



        action = TexasHoldemAction("Call_50")
        infos,public_state, person_states, private_state, action_history  = env.forward(action)
        assert(public_state[-1].stage == Stage.firstStage)
        print (env.__public_state_history__[-1].num_needed_to_action, env.__public_state_history__[-1].is_needed_to_action)
        print (public_state[-1].stage)
        print (public_state[-1].chips)
        print (public_state[-1].bets)
        print (public_state[-1].param_dealer_id)
        # dealer_id = 0
        # turn  = 2
        # stage = 1
        # chips:40,   440, 980
        # bets :60,   60,  20
        # state:n,   n,  n
        # raise_account: 40
        # expected:f,f,t

        action = TexasHoldemAction("Call_40")
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        print ("\n\n")
        print ("stage",public_state[-1].stage)
        print ("dealer_id+1", (public_state[-1].param_dealer_id+1)%public_state[-1].param_num_normal_players)
        print ("is_needed_to_action", public_state[-1].is_needed_to_action)
        self.assertEqual(infos[0].public_state_history[-1].stage,Stage.secondStage)
        self.assertEqual(env.__public_state_history__[-1].chips[1],440)
        self.assertEqual(env.__public_state_history__[-1].turn, 1)
        # dealer_id = 0
        # turn  = 1
        # stage = 2
        # chips:40,   440, 940
        # bets :60,   60,  60
        # state:n,   n,  n
        # raise_account: 40


        action = TexasHoldemAction("Check_0")
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        self.assertEqual(env.__public_state_history__[-1].stage,3)
        self.assertEqual(len(env.__public_state_history__[-1].public_cards),4)
        p = 0
        tmp = [roomai.games.texasholdem.PokerCard(3, 1), roomai.games.texasholdem.PokerCard(4, 2),
               roomai.games.texasholdem.PokerCard(5, 3), roomai.games.texasholdem.PokerCard(6, 0)]
        self.assertEqual(env.__public_state_history__[-1].raise_account, 40)
        self.assertEqual(env.__public_state_history__[-1].stage, 3)
        self.assertEqual(env.__public_state_history__[-1].turn, 1)
        print ("1", infos[1].person_state_history[-1].available_actions.keys())
        # dealer_id = 0
        # turn  = 1
        # stage = 3
        # chips:40,  440, 940
        # bets :60,   60,  60
        # state:n,   n,  n
        # raise_account: 40


        action = TexasHoldemAction("Allin_440")
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        self.assertEqual(infos[0].public_state_history[-1].max_bet_sofar, 500)
        print ("2", infos[2].person_state_history[-1].available_actions.keys())
        self.assertEqual(env.__public_state_history__[-1].is_allin[1],True)
        self.assertEqual(infos[0].public_state_history[-1].stage, 3)
        # dealer_id = 0
        # turn  = 2
        # stage = 3
        # chips:40,   0, 940
        # bets :60,   500,  60
        # state:n,   n,  n
        # raise_account: 40


        action = TexasHoldemAction("Call_440")
        infos,public_state, person_states, private_state,action_history = env.forward(action)
        action = TexasHoldemAction("Allin_40")
        infos,public_state, person_states, private_state,action_history  = env.forward(action)
        # dealer_id = 0
        # chips:0,     0,    500
        # bets :100,   500,  500
        # 0 > 1 = 2

        self.assertEqual(public_state[-1].scores[0],200.0/public_state[-1].param_big_blind_bet)
        self.assertEqual(public_state[-1].scores[1],-100.0/public_state[-1].param_big_blind_bet)
        self.assertEqual(public_state[-1].scores[2],-100.0/public_state[-1].param_big_blind_bet)



    def testEnv2players(self):
        """

        """
        env = TexasHoldemEnv()
        env.num_normal_players = 2

    def testRandomPlayer(self):
        """

        """

        random.seed(0)

        for i in range(100):
            players = [RandomPlayer() for i in range(4)]

            env = TexasHoldemEnv()
            num_normal_players = 3
            chips       = [1000 for i in range(num_normal_players)]
            params = {"param_num_normal_players": num_normal_players,  "chips": chips}
            infos, public_state_history, person_states_history, private_state_history, action_history  = env.init(params)

            while public_state_history[-1].is_terminal != True:
                for i in range(4):
                    players[i].receive_info(infos[i])
                turn   = public_state_history[-1].turn
                action = players[turn].take_action()

                infos, public_state_history, person_states_history, private_state_history, action_history = env.forward(action)



        for i in range(100):
            players = [RandomPlayer() for i in range(3)]

            env = TexasHoldemEnv()
            num_normal_players = 2
            chips     = [1000 for i in range(num_normal_players)]
            dealer_id = i%2
            params = {"param_num_normal_players": num_normal_players, "dealer_id": dealer_id, "chips": chips}
            infos, public_state, person_states, private_state, action_history = env.init(params)

            while public_state[-1].is_terminal != True:
                for i in range(num_normal_players+1):
                    players[i].receive_info(infos[i])
                turn   = public_state[-1].turn
                action = players[turn].take_action()

                infos, public_state, person_states, private_state, action_history= env.forward(action)

    def testCompete(self):
        """

        """
        import random
        random.seed(100)
        players = [RandomPlayer() for i in range(5)]
        env = TexasHoldemEnv()

        scores = TexasHoldemEnv.compete_silent(env, players)
        print (scores)


    def testTextPlayer(self):
        roomai.games.texasholdem.TexasHoldemExample.main(roomai.games.common.RandomPlayerChance(),roomai.games.common.RandomPlayerChance(),roomai.games.common.RandomPlayerChance())
