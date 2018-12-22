# Guides for Game Developers
Before read this, please read the [tutorial](tutorials.md).

This is some guides for developers, who want to add some games into RoomAI. There are some common steps.
- [Step 1: Choose the Game](#step-1-choose-the-game)
- [Step 2: Make the Game into the Extensive Form Game](#step-2-make-the-game-into-the-extensive-form-game)
- [Step 3: Implement the Game](#step-3-implement-the-game)
- [Step 4: Test](#step-4-test)
- [Step 5: Documents](#step-5-documents)

#### Step 1: Choose the Game

The first step is to choose the game, which you want to add into RoomAI. The game should be a imperfect information game, so that Go, Chess and Chinese Chess are excluded from the candidate list.

We choose Kuhn Poker for example in this document. Kuhn Poker is an extremely simplified form of poker developed by Harold W. Kuhn as a simple model zero-sum two-player imperfect-information game

1. Each player is dealt one of three numbers (0,1,2), and the third number will be unseen.
1. Player 0 can check or bet.
    1. If player 0 checks then player 1 can check or bet.
        1.  If player 1 checks there is a showdown (i.e. the higher number wins 1 from the other player).
        1.  If player 1 bets then player 0 can check or bet.
            1.  If player 0 checks then player 1 wins 1 from player 0.
            1.  If player 0 bets there is a showdown (i.e. the higher number wins 2 from the other player).
    1.  If player 0 bets then player 1 can check or bet.
        1.  If player 1 checks then player 0 wins 1 from player 1.
        1.  If player 1 bets there is a showdown (i.e. the higher number wins 2 from the other player).
        


#### Step 2: Make the Game into the Extensive Form Game.

The difference between the common game and the extensive form game is [the chance player](fqa.md#2-what-is-the-chance-player-).There are some random events in the games. For example, the initialized hand cards in players are due to "Nature". The extensive form game adds "Nature" as a chance player, who decides the samples of these random events. 

To make the game into othe extensive form game, is to add a chance player. In Kuhn Poker, the random event is the number dealt to the players. Hence the extensive form game of Kuhn Poker is as follows:

1. The chance player deals one of 0,1,2 to player 0.
1. The chance player deals one of the rest numbers to player1.
1. Player 0 can check or bet.
    1. If player 0 checks then player 1 can check or bet. 
        1.  If player 1 checks there is a showdown (i.e. the higher number wins 1 from the other player).
        1.  If player 1 bets then player 0 can check or bet.
            1.  If player 0 checks then player 1 wins 1 from player 0.
            1.  If player 0 bets there is a showdown (i.e. the higher number wins 2 from the other player).
    1.  If player 0 bets then player 1 can check or bet.
        1.  If player 1 checks then player 0 wins 1 from player 1.
        1.  If player 1 bets there is a showdown (i.e. the higher number wins 2 from the other player).
 
  
#### Step 3: Implement the Game

To implement a game, you should define some class about the environment, the player, the chance player, the action, the chance action,
the public state, the person state and the private state. In the [tutorials](tutorials.md), we have showed the roles of these classes.  Now we take Kuhn Poker as example to show how to implement the game.

###### KuhnPokerPublicState 

Firstly, we define the KuhnPokerPublicState class. The KuhnPokerPublicState extends roomai.common.AbstractPublicState. Besides the "turn", "is_terminal", "scores", "action_history", "param_start_turn", "param_number_normal_players" and "param_backward_enable" properties from AbstractPublicState,
  we need add "first" property to KuhnPokerPublicState, which indicates which normal player is first to take an action. The code for KuhnPokerPublicState is shown as follows.
  
  <pre>
  class KuhnPokerPublicState(roomai.common.AbstractPublicState):
    '''
    The public state class of the KuhnPoker game
    '''
    def __init__(self):
        super(KuhnPokerPublicState,self).__init__()
        self.__first__                      = 0

    def __get_first__(self):    return self.__first__
    first = property(__get_first__, doc="players[first] is first to take an action")
    ## By this way, The outer class can read "first" but can't modify "first"   
        
    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = KuhnPokerPublicState()
        newinstance = super(KuhnPokerPublicState, self).__deepcopy__(newinstance=newinstance)
        newinstance.__first__ = self.first
        return newinstance
     ## PublicState may been copy.deepcopy and need the __deepcopy__ function to improve the performance.
  </pre>
  
  ###### KuhnPokerPersonState
  Secondly, we define the KuhnPokerPersonState class. The KuhnPokerPersonState extends roomai.common.AbstractPersonState. Besides the "id" and "available_actions" properties from AbstractPersonState,
  we need add "number" property to KuhnPokerPersonState, which indicates which number the corresponding player receives. The code for KuhnPokerPersonState is shown as follows.
   
  
  <pre>
  class KuhnPokerPersonState(roomai.common.AbstractPersonState):
    '''
    The person state of KuhnPoker
    '''
    def __init__(self):
        super(KuhnPokerPersonState,self).__init__()
        self.__number__ = 0

    def __get_number__(self):   return self.__number__
    number = property(__get_number__)
    '''
    The number given by the game enviroment. 
    The value of this number is in {0,1,2}. The larger number, the higher win rate.
    '''

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
           newinstance = KuhnPokerPersonState()
        newinstance =  super(KuhnPokerPersonState, self).__deepcopy__(newinstance = newinstance)
        
        newinstance.__number__ = self.__number__
        return newinstance
    ## PublicState may been copy.deepcopy and need the __deepcopy__ function to improve the performance.
  </pre>
  
  ###### KuhnPokerPrivateState
Thirdly, we define the KuhnPokerPrivateState class. We add no property to the KuhnPokerPrivateState class. Hence the code for this class is as follows.
<pre>
class KuhnPokerPrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state class of KuhnPoker
    '''
    
    def __deepcopy__(self, memodict={}, newinstance = None):
        return AKuhnPokerPrivateState
    # The private_state object may be copy.deepcopy, and needs __deepcopy__ to accelerate. 
AKuhnPokerPrivateState = KuhnPokerPrivateState()
</pre>

  ###### KuhnPokerAction
  Fourthly, we define the KuhnPokerAction class.
  <pre>
  class KuhnPokerAction(roomai.common.AbstractAction):

    def __init__(self, key):
        super(KuhnPokerAction,self).__init__(key)
        self.__key__ = key

    ## All actions in RoomAI have a key as their identifications.
    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the KuhnPoker action, \"bet\" or \"check\".")

    ## Since the actions in RoomAI need be constructed repeatly, we construct all actions at the import stage.
    ## Hence we need a static lookup function to access the specified action.
    @classmethod
    def lookup(cls, key):
        return AllKuhnActions[key]
    
    ## The action may be copy.deepcopy.
    def __deepcopy__(self, memodict={}, newinstance = None):
        return KuhnPokerAction.lookup(self.key)

AllKuhnActions = {"bet":KuhnPokerAction("bet"),"check":KuhnPokerAction("check")}

  </pre>
  
  ###### KuhnPokerActionChance
  Fifthly, we define the KuhnPokerActionChance class. The KuhnPokerActionChance class represents an action used the chance player.
  <pre>
  ### All chance action classes' name is xxxChance
  class KuhnPokerActionChance(roomai.common.AbstractAction):
    def __init__(self, key):
        super(KuhnPokerActionChance, self).__init__(key)
        self.__key__ = key
        n1_n2        = key.split(",")
        self.__number_for_player0 = int(n1_n2[0])
        self.__number_for_player1 = int(n1_n2[1])

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the KuhnPokerChance action, for example, \"0,1\"")

    def __get_number_for_player0__(self):
        return self.__number_for_player0
    number_for_player0 = property(__get_number_for_player0__, doc = "The number of the players[0]")

    def __get_number_for_player1__(self):
        return self.__number_for_player1
    number_for_player1 = property(__get_number_for_player1__, doc = "The number of the players[1]")

    @classmethod
    def lookup(cls, key):
        return AllKuhnChanceActions[key]

    def __deepcopy__(self, memodict={}, newinstance=None):
        return KuhnPokerActionChance.lookup(self.key)

AllKuhnChanceActions = {"0,1": KuhnPokerActionChance("0,1"), \
                        "1,0": KuhnPokerActionChance("1,0"),\
                        "0,2": KuhnPokerActionChance("0,2"), \
                        "2,0": KuhnPokerActionChance("2,0"), \
                        "1,2": KuhnPokerActionChance("1,2"), \
                        "2,1": KuhnPokerActionChance("2,1"), }
  </pre>
  ###### KuhnPokerEnv
  Defining the KuhnPokerPublicState, KuhnPokerPersonState, KuhnPokerPrivateState, KuhnPokerAction and KuhnPokerActionChance classes is to prepare for defining KuhnPokerEnv.
  
  
  The KuhnPokerEnv class extends roomai.common.AbstractEnv, and has the \__params\__, public_state, person_states, private_state and other internal properties. You only need to be concerned with the \__params\__, public_state, person_states and private_state properties, and are required not to add new property.
  
  The KuhnPokerEnv has five un-implemented functions:init, forward, \__deepcopy\__, compete (static function), available_actions(static function).
  
  - init
  
  The init function is to initialize the environment for a new game, which sets the initialized values in the public_state, person_states and private_state properties using the params. The init function code for Kuhn Poker is shown
   <pre>
   def init(self, params=dict()):
        '''
        Initialize the KuhnPoker game environment.The params is the initialization params with the following params:\n
        1. param_backward_enable: If you need call the backward function of the enviroment, please set it to True. Default False.
        2. param_start_turn: The param_start_turn is the id of a normal player, who is the first to take an action. In KuhnPoker, param_start_turn must be 0 or 1.
        #### For this init function, we should show the params
        
        :param params: the initialization params, for example, params={"param_start_turn":1}
        :return: infos, public_state, person_states, private_state 
        '''
        #### You must use reStructureText Docstring format to write the comment.


        self.private_state = roomai.kuhnpoker.KuhnPokerPrivateState()
        self.public_state  = roomai.kuhnpoker.KuhnPokerPublicState()
        self.person_states = [roomai.kuhnpoker.KuhnPokerPersonState() for i in range(3)]

        if "param_backward_enable" in params:
            self.public_state.__param_backward_enable__ = params["param_backward_enable"]
        else:
            self.public_state.__param_backward_enable__ = False

        if "param_start_turn" in params:
            self.public_state.__param_start_turn__ = params["start_turn"]
        else:
            self.public_state.__param_start_turn__ = int(random.random() * 2)
        if self.public_state.__param_start_turn__ not in [0,1]:
            raise ValueError("The param_start_turn (%d) must be in [0,1]"%(self.public_state.__param_start_turn__))

        if "param_num_normal_players" in params:
            logger.warning(
                "KuhnPoker is a game of two players and the number of players always be 2. Ingores the \"num_normal_players\" option")
        self.public_state.__param_num_normal_players__= 2

        self.public_state.__turn__             = 2
        self.public_state.__first__            = self.public_state.__param_start_turn__
        self.public_state.__epoch__            = 0
        self.public_state.__action_history__   = []
        self.public_state.__is_terminal__      = False
        self.public_state.__scores__           = None
        self.person_states[0].__id__           = 0
        self.person_states[0].__number__       = -1
        self.person_states[1].__id__           = 1
        self.person_states[1].__number__       = -1
        self.person_states[2].__id__           = 2
        self.person_states[2].__number__       = -1

        self.person_states[self.public_state.turn].__available_actions__ = roomai.kuhnpoker.AllKuhnChanceActions

       
        self.__gen_state_history_list__()  
        ### Call self.__gen_state_history_list__() before return statement
        return  self.__gen_infos__(), self.public_state, self.person_states, self.private_state
   </pre>
   
  - forward
  
  The forward function makes the environment to step foward with the given action. The forward function generates the available actions for the next turn player using the available_actions function.  
  
  <pre>
      def forward(self, action):
        """
        The KuhnPoker game environment steps with the action taken by the current player
        :param action
        :returns:infos, public_state, person_states, private_state
        """
        #### You must use reStructureText Docstring format to write the comment.
        

        ####### forward with the chance action ##########
        if isinstance(action, roomai.kuhnpoker.KuhnPokerActionChance) == True:
            self.public_state.__action_history__.append((2,action))
            self.person_states[0].__number__ = action.number_for_player0
            self.person_states[1].__number__ = action.number_for_player1
            self.person_states[self.public_state.turn].__available_actions__ = dict()
            self.public_state.__turn__ = self.public_state.__param_start_turn__
            self.person_states[self.public_state.turn].__available_actions__ = self.available_actions(self.public_state, self.person_states[self.public_state.turn])
            
            self.__gen_state_history_list__()
            ### Call self.__gen_state_history_list__() before return statement
            
            return self.__gen_infos__(), self.public_state, self.person_states, self.private_state



        self.person_states[self.public_state.turn].__available_actions__ = dict()
        self.public_state.__action_history__.append((self.public_state.turn,action))
        #self.public_state.__epoch__                                     += 1
        self.public_state.__turn__                                       = (self.public_state.turn+1)%2


        if len(self.public_state.action_history) == 1: #1 chance
            pass
        elif len(self.public_state.action_history) == 1+1: #1 normal + 1 chance
            self.public_state.__is_terminal__ = False
            self.public_state.__scores__      = []
            self.person_states[self.public_state.turn].__available_actions__ = roomai.kuhnpoker.AllKuhnActions

            self.__gen_state_history_list__()
            ### Call __gen_state_history_list__() before the return statement 
            return self.__gen_infos__(), self.public_state, self.person_states, self.private_state

        elif len(self.public_state.action_history) == 2+1: # 2 normal + 1 chance
            scores = self.__evalute_two_round__()
            if scores is not None:
                self.public_state.__is_terminal__ = True
                self.public_state.__scores__      = scores

                self.__gen_state_history_list__()
                ### Call __gen_state_history_list__() before the return statement 
                return self.__gen_infos__(),self.public_state, self.person_states, self.private_state
            else:
                self.public_state.__is_terminal__ = False
                self.public_state.__scores__      = []
                self.person_states[self.public_state.turn].__available_actions__ = roomai.kuhnpoker.AllKuhnActions

                self.__gen_state_history_list__()
                __gen_state_history_list__()
                ### Call __gen_state_history_list__() before the return statement 
                return self.__gen_infos__(),self.public_state, self.person_states, self.private_state

        elif len(self.public_state.action_history) == 3 + 1: # 3 normal action + 1 chance
            self.public_state.__is_terminal__ = True
            self.public_state.__scores__     = self.__evalute_three_round__()

            self.__gen_state_history_list__()
            ### Call __gen_state_history_list__() before the return statement 
            return self.__gen_infos__(),self.public_state, self.person_states, self.private_state

        else:
            raise Exception("KuhnPoker has 4 items in action_history (3 normal actions + 1 chance action)")
   </pre>
   
    
  - \__deepcopy\__
  
  The \__deepcopy\__ is used for accelerating copy.deepcopy. Just copy the following code.
<pre> 
def __deepcopy__(self, memodict={}, newinstance = None):
   if newinstance is None:
      newinstance = XXXEnv ## chang it to your game name.
   newinstance = super(XXXEnv, self).__deepcopy__(newinstance=newinstance)
   return newinstance
</pre>
  
  - compete. 
  
  The compete function is a static function. The compete function holds a compete for the players with an environment, and competes scores for players. The compete function code for Kuhn Poker is shown.
  <pre>
  @classmethod
  def compete(cls,env, players)
       '''
       Use the game environment to hold a compete for the players
       :param env: The game environment
       :param players: The players
       :return: scores for the players
       '''

       if len(players) != 3:
          raise  ValueError("The len(players) in Kuhn is 3 (2 normal players and 1 chance player).")


       infos, public_state, person_state, private_state = env.init()
       for i in range(len(players)):
           players[i].receive_info(infos[i])

       while public_state.is_terminal == False:
           turn = infos[-1].public_state.turn
           action = players[turn].take_action()
           infos,public_state, person_state, private_state = env.forward(action)
           for i in range(len(players)):
               players[i].receive_info(infos[i])
 </pre>
  
  - available_actions

  The available_actions is a static function, and generates available actions for the next normal player. The available actions for the chance player is out of this function.  The available_actions code for Kuhn Poker is shown.
  <pre>
  def available_actions(self, public_state, person_state):
       return roomai.kuhnpoker.AllKuhnActions
  </pre>
  
  
###### Requirements
There are some requirements for implementation:
1. Write Python 2/3 compatible code to implement your game.
1. Put each class in one script file. 




#### Step 4: Test

Write the unittest code to ensure the correctness of your game. Improve the performance of your game. The suggestion baseline of the performance is
100 competitions per second with 4-6 random players.

#### Step 5: Documents

Write the comments using the reStructureText Docstring format.


 


