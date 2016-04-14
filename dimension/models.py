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
TBD
"""

bibliography = (
    (
        'TBD'
    ),
)


class Constants(BaseConstants):
    name_in_url = 'dimension'
    players_per_group = 4
    num_rounds = 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for i, group in enumerate(self.get_groups()):
            group.num_prices = 2 # TODO: vary by group!

            group_roles = self.generate_roles()
            for player, role in zip(group.get_players(), group_roles):
                player.participant.vars['role'] = role

    @staticmethod
    def generate_roles():
        num = int(Constants.players_per_group / 2)
        roles = ['buyer'] * num + ['seller'] * num
        random.shuffle(roles)
        return roles


class Group(BaseGroup):
    num_prices = models.PositiveIntegerField()


class Player(BasePlayer):
    buyer_choice = models.PositiveIntegerField(null=True, blank=True)
    buyer_total = models.CurrencyField(null=True, blank=True)

    seller_price0 = models.CurrencyField(null=True, blank=True)
    seller_price1 = models.CurrencyField(null=True, blank=True)
    seller_price2 = models.CurrencyField(null=True, blank=True)
    seller_price3 = models.CurrencyField(null=True, blank=True)
    seller_price4 = models.CurrencyField(null=True, blank=True)
    seller_price5 = models.CurrencyField(null=True, blank=True)
    seller_price6 = models.CurrencyField(null=True, blank=True)
    seller_price7 = models.CurrencyField(null=True, blank=True)
