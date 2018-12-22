#!/bin/python
#coding:utf-8
import random
import roomai.games.common
import roomai.games.kuhnpoker.KuhnPokerActionChance

class KuhnPokerChancePlayer(roomai.games.common.AbstractPlayer):
    def receive_info(self, info):
        self.available_actions_list = list(info.person_state.available_actions.values())
    def take_action(self):
        action =  random.choice(self.available_actions_list)
        return action
    def reset(self):
        pass

class Example_KuhnPokerAlwaysBetPlayer(roomai.games.common.AbstractPlayer):
    def receive_info(self, info):
        pass     

    def take_action(self):
        return roomai.kuhnpoker.KuhnPokerAction("bet")

    def reset(self):
        pass


