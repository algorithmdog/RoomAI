#!/bin/python
import random
import copy
from random import choice

import roomai
from roomai.games.common import AbstractEnv
from roomai.games.bang   import BangActionChance
from roomai.games.bang   import BangStatePublic
from roomai.games.bang   import BangStatePrivate
from roomai.games.bang   import BangStatePerson
from roomai.games.bang   import PublicPersonInfo

from roomai.games.bang   import AllCharacterCardsDict
from roomai.games.bang   import PlayingCardNames
from roomai.games.bang   import CardRole

class BangEnv(AbstractEnv):


    def init(self, params = dict()):
        '''
        Initialize the TexasHoldem game environment with the initialization params.\n
        The initialization is a dict with only an option: \n
        param_num_normal_players: how many players are in the game, the option must be in {2, 4, 5}, default 5. An example of the initialization param is {"param_num_normal_players":2} \n
        
        :param params: the initialization params
        :return: infos, public_state, person_states, private_state
        '''


        logger         = roomai.get_logger()
        public_state   = BangStatePublic()
        private_state  = BangStatePrivate()

        if "param_num_normal_players" in params:
            public_state.__param_num_normal_players__ = params["param_num_normal_players"]
        else:
            public_state.__param_num_normal_players__ = 5

        if public_state.param_num_normal_players not in [2,4,5]:
            logger.fatal("The number of normal players must be in [2,4,5]")
            raise ValueError("The number of normal players must be in [2,4,5]")

        public_state.__public_person_infos__ = [PublicPersonInfo() for i in range(public_state.__param_num_normal_players__)]
        for i in range(public_state.__param_num_normal_players__):
            public_state.__public_person_infos__[i].__num_hand_cards__ = 0
            public_state.__public_person_infos__[i].__character_card__ = None

            public_state.__public_person_infos__[i].__equipment_cards__ = []

        person_states = [BangStatePerson() for i in range(public_state.param_num_normal_players+1)]

        self.__public_state_history__.append(public_state)
        self.__private_state_history__.append(private_state)
        for i in range(public_state.param_num_normal_players):
            self.__person_states_history__[i].append(person_states[i])
            self.__person_states_history__[i][0].__id__         = i
            self.__person_states_history__[i][0].__hand_cards__ = []
            self.__person_states_history__[i][0].__role__       = ""
        self.__person_states_history__[public_state.__param_num_normal_players__][0].__available_actions__ = self.available_actions()
        

        self.__gen_infos__()


    def forward(self, action):

        """
        接受一个动作，先检查是否是ActionChance，处理，如果是正常玩家的，pass
        如果是ActionChance，进行相应的动作处理

        The Bang game environment steps with the action taken by the current player

        :param action
        :returns:infos, public_state, person_states, private_state
        """
        private_state = copy.deepcopy(self.__private_state_history__[-1])
        public_state = copy.deepcopy(self.__public_state_history__[-1])
        person_states = [copy.deepcopy(self.__person_states_history__[i][-1]) for i in range(public_state.param_num_normal_players)]

        self.__public_state_history__.append(public_state)
        self.__private_state_history__.append(private_state)
        for i in range(len(person_states)):
            self.__person_states_history__[i].append(person_states[i])

        if action.type == BangActionChance.BangActionChanceType.charactercard:  # chance player deals character cards
            person_states[public_state.turn].__available_actions__ = self.available_actions()
            for i in range(len(public_state.__public_person_infos__)):
                if public_state.__public_person_infos__[i].__character_card is None:  # sample a character card to that player
                    public_state.__public_person_infos__[i].__character_card = \
                        person_states[public_state.turn].__available_actions__[choice(person_states[public_state.turn].__available_actions__.keys)]
                    return self.__gen_infos__(), self.__public_state_history__, self.__person_states_history__, self.__private_state_history__
            # if all players have been assigned a character, return
            return self.__gen_infos__(), self.__public_state_history__, self.__person_states_history__, self.__private_state_history__

        if action.type == BangActionChance.BangActionChanceType.rolecard: # chance player deals role cards
            person_states[public_state.turn].__available_actions__ = self.available_actions()
            for i in range(public_state.param_num_normal_players):
                if person_states[i].__role__ is None:  # sample a role card to that player
                    person_states[i].__role__ = person_states[public_state.turn].__available_actions__[choice(person_states[public_state.turn].__available_actions__.keys)]
                    if person_states[i].__role__ == CardRole.RoleCard(CardRole.RoleCardNames.sheriff):
                        public_state.__sheriff_id__ = i

        if action.type == BangActionChance.BangActionChanceType.normalcard:  # chance player shuffle cards
            if len(private_state.library) == 0:  # there is no card, and the chance player needs to shuffle discard cards
                private_state.__library__ = copy(public_state.__discard_pile__)

        person_states[public_state.turn].__available_actions__ = dict()
        public_state.__turn__ = (public_state.turn + 1) % 2

    def available_actions(self):
        '''
        Generate all valid actions given the public state and the person state

        :return: all valid actions
        '''
        logger = roomai.get_logger()
        ## charactercard

        if self.__public_state_history__[-1].__public_person_infos__[-1].__character_card__ is None:
            available_actions = dict()
            tmp_set = set()
            for i in range(len(self.__public_state_history__[-1].__public_person_infos__)):
                if self.__public_state_history__[-1].__public_person_infos__[i].__character_card__ is not None:
                    tmp_set.add(self.__public_state_history__[-1].__public_person_infos__[i].__character_card__.key)

            for key in AllCharacterCardsDict:
                if key not in tmp_set:
                    available_actions[key] = BangActionChance.lookup(key)
            return available_actions

        ## rolecard
        for i in range(self.__public_state_history__[-1].param_num_normal_players):
            if self.__person_states_history__[i].person_states[-1].__role_card__ is None:
                available_actions = dict()
                tmp_set = set()
                num_sheriff = 0
                num_deputy_sheriff = 0
                num_renegade = 0
                num_outlaw = 0

                for j in range(len(self.__public_state_history__[-1].param_num_normal_players)):
                    if self.__person_states_history__[j].person_states[-1].__role_card__ is not None:
                        tmp_set.add(self.__person_states_history__[j].person_states[-1].__role_card__.key)

                if self.__public_state_history__[-1].__param_num_normal_players__ == 2:
                    return available_actions

                elif self.__public_state_history__[-1].__param_num_normal_players__ == 4:
                    num_sheriff = 1
                    num_renegade = 1
                    num_outlaw = 2

                elif self.__public_state_history__[-1].__param_num_normal_players__ == 5:
                    num_sheriff = 1
                    num_deputy_sheriff = 1
                    num_renegade = 1
                    num_outlaw = 2

                else:
                    logger.fatal("param_num_normal_players not in [2,4,5]")
                    raise ValueError("param_num_normal_players not in [2,4,5]")

                for key in tmp_set:
                    if key == CardRole.RoleCardNames.sheriff:
                        num_sheriff = num_sheriff - 1
                    if key == CardRole.RoleCardNames.deputy_sheriff:
                        num_deputy_sheriff = num_deputy_sheriff - 1
                    if key == CardRole.RoleCardNames.renegade:
                        num_renegade = num_renegade - 1
                    if key == CardRole.RoleCardNames.outlaw:
                        num_outlaw = num_outlaw - 1
                if num_sheriff > 0:
                    available_actions[CardRole.RoleCardNames.sheriff] = BangActionChance.lookup(CardRole.RoleCardNames.sheriff)
                if num_deputy_sheriff > 0:
                    available_actions[CardRole.RoleCardNames.deputy_sheriff] = BangActionChance.lookup(CardRole.RoleCardNames.deputy_sheriff)
                if num_renegade > 0:
                    available_actions[CardRole.RoleCardNames.renegade] = BangActionChance.lookup(CardRole.RoleCardNames.renegade)
                if num_outlaw > 0:
                    available_actions[CardRole.RoleCardNames.outlaw] = BangActionChance.lookup(CardRole.RoleCardNames.outlaw)
                return available_actions

        ##
        available_actions = dict()
        turn = self.__public_state_history__[-1].__turn__
        person_state = self.__person_states_history__[turn][-1]
        for card in person_state.hand_cards:
            if card.name == PlayingCardNames.Duello:
                available_actions[card.key] = Bang
            elif card.name == PlayingCardNames.Carabine:
                pass
            elif card.name == PlayingCardNames.Bang:
                pass
            elif card.name == PlayingCardNames.Emporia:
                pass
            elif card.name == PlayingCardNames.Volcanic:
                pass
            elif card.name == PlayingCardNames.Schofield:
                pass
            elif card.name == PlayingCardNames.Remington:
                pass
            elif card.name == PlayingCardNames.Panic:
                pass
            elif card.name == PlayingCardNames.Dynamite:
                pass
            elif card.name == PlayingCardNames.WellsFargo:
                pass
            elif card.name == PlayingCardNames.Prigione:
                pass
            elif card.name == PlayingCardNames.Saloon:
                pass
            elif card.name == PlayingCardNames.Beer:
                pass
            elif card.name == PlayingCardNames.Catling:
                pass
            elif card.name == PlayingCardNames.CatBalou:
                pass
            elif card.name == PlayingCardNames.Miss:
                pass
            elif card.name == PlayingCardNames.StageCoach:
                pass
            elif card.name == PlayingCardNames.Barrel:
                pass
            elif card.name == PlayingCardNames.Mustang:
                pass
            elif card.name == PlayingCardNames.Indian:
                pass
            elif card.name == PlayingCardNames.Winchester:
                pass
            elif card.name == PlayingCardNames.Appaloosa:
                pass
