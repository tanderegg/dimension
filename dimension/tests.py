# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        self.submit(views.Introduction)
        self.submit(views.Introduction1)
        self.submit(views.Introduction2)
        self.submit(views.Introduction3)
        self.submit(views.GameInstruction)
        self.submit(views.GameInstructions2)
        
    def validate_play(self):
        pass


    Introduction,
    Introduction1,
    Introduction2,
    Introduction3,
    GameInstruction,
    GameInstructions2,
    SetPrices,
    BuyerWaitPage,
    SelectSeller,
    ResultsWaitPage,
    Results,