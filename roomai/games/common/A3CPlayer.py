#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author  : SiFaXie
# @Date    : 2018/12/23
# @Email   : sifaxie@tencent.com
# @File    : A3CPlayer.py
# @Desc    :

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : SiFaXie
# @Date    : 2018/12/23
# @Email   : sifaxie@tencent.com
# @File    : A3C_Player.py
# @Desc    :


import roomai.games.common
from roomai.games.common.AbstractPlayer import AbstractPlayer
from roomai.models.algorithms import AbstractA3C
logger = roomai.get_logger()

class A3CPlayer(AbstractPlayer):
    '''
    The abstract class of a a3c player
    '''

    def __init__(self):
        raise NotImplementedError("The receiveInfo function hasn't been implemented")

    def get_state_spce(self):
        raise NotImplementedError("The receiveInfo function hasn't been implemented")
