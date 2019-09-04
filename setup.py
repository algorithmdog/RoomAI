#!/bin/python
##test
from setuptools import setup

setup(  name        = "roomai",
        version     = "0.1.16",
        description = "A toolkit for developing and comparing imperfect information game bots",
        url         = "https://github.com/roomai/RoomAI",
        author      = "RoomAI Dev",
        author_email= "lili1987mail@gmail.com",
        license     = "MIT",
        packages    = ["roomai","roomai.games","roomai.games.bang","roomai.games.common","roomai.games.texasholdem","roomai.games.kuhnpoker","roomai.models","roomai.models.algorithms","roomai.models.bang","roomai.models.texasholdem"],
        zip_safe    = True)
