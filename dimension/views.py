# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage


def vars_for_all_templates(self):
    return {'instructions': 'dimension/Instructions.html'}


class Introduction(Page):
    template_name = 'global/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1


class SetPrices(Page):
    template_name = 'dimension/SetPrices.html'
    form_model = models.Player

    def is_displayed(self):
        return 'seller' == self.player.participant.vars['role']

    def get_form_fields(self):
        return [
            'seller_price{}'.format(i)
            for i in range(self.group.num_prices)
        ]

    def vars_for_template(self):
        return {'num_prices': self.group.num_prices}


class SelectSeller(Page):
    template_name = 'dimension/SelectSeller.html'
    form_model = models.Player
    form_fields = ('buyer_choice',)

    def is_displayed(self):
        return 'buyer' == self.player.participant.vars['role']

    def vars_for_template(self):
        return {
            'sellers': filter(
                lambda p: 'seller' == p.role,
                self.group.get_players()
            ),
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [
    Introduction,
    SetPrices,
    SelectSeller,
    ResultsWaitPage,
    Results,
]
