#!/bin/python


### test
import roomai.common
import roomai.texas

if __name__ == "__main__":
    random_players = [roomai.common.RandomPlayer() for i in range(3)]
    env = roomai.texas.TexasHoldemEnv()
    for i in range(5):
        env.compete(env, random_players)
