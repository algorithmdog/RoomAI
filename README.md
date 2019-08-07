This project is stoped since there are better projects:

https://github.com/dickreuter/Poker

https://github.com/ishikota/PyPokerEngine

# RoomAI

[![Build Status](https://travis-ci.org/roomai/RoomAI.svg?branch=master)](https://travis-ci.org/roomai/RoomAI.svg?branch=master)
[![Documentation Status](https://readthedocs.org/projects/roomai/badge/?version=latest)](http://roomai.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/roomai.svg)](https://pypi.python.org/pypi/roomai)



RoomAI is a toolkit for developing AI-bots of KuhnPoker, Texas Holdem and Bang!.


# Install and Get Started

You can install roomai with pip

<pre>
pip install roomai
</pre>

try your first AI-bot


<pre>
#!/bin/python
from roomai.games. import *;
import roomai.common

class KuhnPokerExamplePlayer(roomai.games.common.AbstractPlayer):
    def receive_info(self, info):
        if info.person_state_history[-1].available_actions is not None:
            self.available_actions = info.person_state_history[-1].available_actions

    def take_action(self):
        values = self.available_actions.values()
        return list(values)[int(random.random() * len(values))]

    def reset(self):
        pass

if __name__ == "__main__":
        players = [KuhnPokerExamplePlayer() for i in range(2)] + [roomai.games.common.RandomPlayerChance()]
        # RandomChancePlayer is the chance player with the uniform distribution over every output
        env = roomai.games.kuhnpoker.KuhnPokerEnv()
        scores = env.compete_silent(env, players)
        print(scores)
</pre>



# For More Information

 - [Introductions](docs/document/tutorials.md)
 
 - [Tutorials](docs/document/guides_ai.md)
 
 - [Model Zoo](docs/document/model_zoo.md)
 
 - [API Docs](http://roomai.readthedocs.io/en/latest/?badge=latest)
 
 
 - [FQA](docs/document/fqa.md)
 

# Contributors

If you would like to contribute to the project, please send me (lili1987mail at gmail.com) an email. We are always happy for more help.
