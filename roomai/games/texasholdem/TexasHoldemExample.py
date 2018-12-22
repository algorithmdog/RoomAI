#!/bin/python
import random

import roomai.games.common
import roomai.games.texasholdem

random.seed(4)
class Player(roomai.games.common.AbstractPlayer):
    def receive_info(self, info):
        available_actions = info
    def take_action(self):
        action = input("choosed_acton:")
        #action = ""
        return roomai.games.texasholdem.TexasHoldemAction.lookup(action)
    def reset(self):
        pass


def show_public(public_state):
    print ("dealer_id:%d\n"%(public_state.param_dealer_id) +\
           "chips:%s"%(",".join([str(i) for i in public_state.chips])) +\
           "  bets:%s"%(",".join([str(i) for i in public_state.bets])) +\
           "  is_folds:%s\n"%(",".join([str(i) for i in public_state.is_fold])) +\
           "  public_cards:%s"%(",".join([c.key for c in public_state.public_cards]))
           )
def show_info(info):
    person_state          = info.person_state_history[-1]
    print ("%d available_actions: %s" % (person_state.id, ",".join(sorted(person_state.available_actions.keys()))))
    print ("%d cards:%s"%(person_state.id,",".join([c.key for c in person_state.hand_cards])))


def main(player1,player2,player3):
    players     = [player1, player2, player3, roomai.games.common.RandomPlayerChance()]
    env         = roomai.games.texasholdem.TexasHoldemEnv()

    num_players = len(players)
    infos, public_state_history, person_states_history, private_state_history, playerid_action_history = env.init({"num_normal_players": num_players-1})
    show_public(public_state_history[-1])
    for i in range(num_players):
        players[i].receive_info(infos[i])
        show_info(infos[i])
    print ("\n")


    while public_state_history[-1].is_terminal == False:
        turn = public_state_history[-1].turn
        action = players[turn].take_action()
        print ("%d player take an action (%s)"%(turn,action.key))
        infos, public_state_history, person_states_history, private_state_history, playerid_action_history = env.forward(action)
        show_public(public_state_history[-1])
        for i in range(num_players):
            players[i].receive_info(infos[i])
            show_info(infos[i])
        print ("\n")

    print (public_state_history[-1].scores)

if __name__ == "__main__":
    main(Player(),Player(),Player())