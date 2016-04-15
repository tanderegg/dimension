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

class Introduction1(Page):
    template_name = 'dimension/Introduction1.html'

class Introduction2(Page):
    template_name = 'dimension/Introduction2.html'

    def vars_for_template(self):
        return {'num_rounds': models.Constants.num_rounds}

class Introduction3(Page):
    template_name = 'dimension/Introduction3.html'

class GameInstruction(Page):
    template_name = 'dimension/GameInstruction.html'

class GameInstructions2(Page):
    template_name = 'dimension/GameInstructions2.html'

class SetPrices(Page):
    template_name = 'dimension/SetPrices.html'
    form_model = models.Player

    def is_displayed(self):
        return 'seller' == self.player.participant.vars['role']

    def get_form_fields(self):
        print([
            'seller_price{}'.format(i)
            for i in range(self.group.num_prices)
            ])
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
        print self.group.get_players()
        return {
            'sellers': enumerate(filter(
                lambda p: 'seller' == p.participant.vars['role'],
                self.group.get_players()
            )),
        }


class BuyerWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        # TODO: compute final results
        pass


class Results(Page):
    pass


page_sequence = [
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
]
