import roomai
import roomai.games.common
import roomai.games.kuhnpoker
import random
import unittest

class KuhnPokerExamplePlayer(roomai.games.common.AbstractPlayer):
    def receive_info(self, info):
        if info.person_state_history[-1].available_actions is not None:
            self.available_actions = info.person_state_history[-1].available_actions

    def take_action(self):
        values = self.available_actions.values()
        return list(values)[int(random.random() * len(values))]

    def reset(self):
        pass

class KuhnTester(unittest.TestCase):
    def testKuhn(self):
        players = [KuhnPokerExamplePlayer() for i in range(2)] + [roomai.games.common.RandomPlayerChance()]
        # RandomChancePlayer is the chance player with the uniform distribution over every output
        env = roomai.games.kuhnpoker.KuhnPokerEnv()
        scores = env.compete_silent(env, players)
        print(scores)