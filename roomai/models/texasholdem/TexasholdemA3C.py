#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author  : SiFaXie
# @Date    : 2018/12/23
# @Email   : sifaxie@tencent.com
# @File    : TexasholdemA3C.py
# @Desc    :
import multiprocessing
import os
import threading

import numpy as np
import tensorflow as tf

import shutil
import roomai
from roomai.models.algorithms.AbstractA3C import AbstractA3C
from roomai.games.common import RandomPlayer
from roomai.models.texasholdem import Texasholdem_A3CPlayer
from roomai.games.texasholdem import *


def  TexasholdemA3C_Train():
    env = roomai.games.texasholdem.TexasHoldemEnv()

    random_player = RandomPlayer()
    chance_player = roomai.games.common.RandomPlayerChance()
    other_players = [random_player, chance_player]
    params = {"param_num_normal_players": 2,
              "param_init_chips": [100, 100],
              "param_big_blind_bet": 20,
              "backward_enable": True,
              'MAX_GLOBAL_EP': 1000,
              'env': env,
              'otherplayers': other_players,
              'MODEL_DIR':'./checkpoint/TexasHoldemModel'}
    a3c = AbstractA3C([None, 14, 8, 1], 5, params)
    action_dict = {"Fold":0, "Check":1, "Call":2, "Raise":3, "Allin":4}
    a3c.train(action_dict)

def TexasholdemA3C_Predict():
    import random
    random.seed(100)
    state_spec = [None, 14, 8, 1]
    n_a = 5
    a3c_player = Texasholdem_A3CPlayer(state_spec, n_a)
    a3c_player.load_model('./checkpoint','TexasHoldemModel')
    randomp_pleyer = RandomPlayer()
    players = [a3c_player, randomp_pleyer]
    env = TexasHoldemEnv()
    for i in range(100):
        scores = TexasHoldemEnv.compete_silent(env, players)
        print(scores)


if __name__ =='__main__':
    # texasholdema3c_train = TexasholdemA3C_Train()
    TexasholdemA3C_Predict()