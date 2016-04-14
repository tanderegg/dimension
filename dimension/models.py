# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
a description of this game.
"""

class Constants(BaseConstants):
    players_per_group = 4
    name_in_url = 'bertrand_competition'
    num_rounds = 1
    bonus = c(10)
    maximum_price = c(100)


class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):


    def set_payoffs(self):
        players = self.get_players()
        winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == winning_price]
        winner = random.choice(winners)
        for p in players:
            p.payoff = Constants.bonus
            if p == winner:
                p.is_a_winner = True
                p.payoff += p.price


class Player(BasePlayer):

    training_my_profit = models.CurrencyField(
        verbose_name='My profit would be')

    price = models.CurrencyField(
        min=0, max=Constants.maximum_price,
        doc="""Price player chooses to sell product for"""
    )

    is_a_winner = models.BooleanField(
        initial=False,
        doc="""Whether this player offered lowest price"""
    )

