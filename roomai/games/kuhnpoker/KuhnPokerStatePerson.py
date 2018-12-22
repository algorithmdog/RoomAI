import roomai.games.common

class KuhnPokerStatePerson(roomai.games.common.AbstractStatePerson):
    '''
    The person state of KuhnPoker
    '''
    def __init__(self):
        super(KuhnPokerStatePerson, self).__init__()
        self.__number__ = 0

    def __get_number__(self):   return self.__number__
    number = property(__get_number__,doc="The number given by the game enviroment. The value of this number is in {0,1,2}. The larger number, the higher win rate")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
           newinstance = KuhnPokerStatePerson()
        newinstance =  super(KuhnPokerStatePerson, self).__deepcopy__(newinstance = newinstance)

        newinstance.__number__ = self.__number__
        return newinstance