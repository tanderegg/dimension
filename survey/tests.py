# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        self.submit(views.Demographics, {
            'q_country': 'BS',
            'q_age': 24,
            'q_gender': 'Male'})

        self.submit(views.RiskQuestions, {
            'q_risk1': 1,
            'q_risk2': 1,
            'q_risk3': 1
        })

    def validate_play(self):
        pass
