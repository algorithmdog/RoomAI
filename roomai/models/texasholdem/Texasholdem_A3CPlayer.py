#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author  : SiFaXie
# @Date    : 2018/12/23
# @Email   : sifaxie@tencent.com
# @File    : Texasholdem_A3CPlayer.py
# @Desc    :


import roomai.games.common
from roomai.games.common.AbstractPlayer import AbstractPlayer
from roomai.models.algorithms import AbstractA3C
logger = roomai.get_logger()
import numpy as np

class Texasholdem_A3CPlayer(AbstractPlayer):

    def __init__(self, state_spec, n_a):
        self.state_spec = state_spec
        self.n_a= n_a
        self.action_dict = {"Fold":0, "Check":1, "Call":2, "Raise":3, "Allin":4}

    def load_model(self, model_path, model_name):
        self.a3c = AbstractA3C(self.state_spec, self.n_a)
        self.a3c.load_model(model_path, model_name)

    def receive_info(self, info):

        self.s = np.zeros((14, 8, 1))
        if (info.public_state_history[-1].param_dealer_id == info.person_state_history[-1].id):
            for card in info.public_state_history[-1].public_cards:
                self.s[card.point_rank, card.suit_rank, 0] = 1
            for card in info.person_state_history[-1].hand_cards:
                self.s[card.point_rank, card.suit_rank, 0] = 1
        else:
            for card in info.public_state_history[-1].public_cards:
                self.s[card.point_rank, card.suit_rank + 4, 0] = 1
            for card in info.person_state_history[-1].hand_cards:
                self.s[card.point_rank, card.suit_rank + 4, 0] = 1
        self.available_action = dict()
        self.available_option = []
        for action in list(info.person_state_history[-1].available_actions.values()):
            option = action.option
            if option not in self.available_option:
                #对于 raise 只取第一个
                self.available_option.append(option)
                self.available_action[option] = action

    def take_action(self):
        a = self.a3c.choose_action(self.s, self.available_option, self.action_dict)
        return self.available_action[a]

    def reset(self):
        passh

