# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage


def vars_for_all_templates(self):
    return {'instructions': 'dimension/Instructions.html'}


class Begin(Page):
    template_name = 'dimension/Begin.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

class PRA(Page):
    template_name = 'dimension/PRA.html'

    def vars_for_template(self):
        self.group.set_identifier()

    def is_displayed(self):
        return self.subsession.round_number == 1


class Introduction(Page):
    template_name = 'dimension/Introduction.html'

    def vars_for_template(self):
        return {'num_rounds': models.Constants.num_rounds, 
        'num_games' : models.Constants.num_games}

class IntroductionPayment(Page):
    template_name = 'dimension/IntroductionPayment.html'

    def vars_for_template(self):
        return {'redeem_value': models.Constants.redeem_value,
        'tokens_per_cent': models.Constants.tokens_per_cent,
        'tokens_per_dollar' : models.Constants.tokens_per_cent*100,
        'starting_tokens' : models.Constants.starting_tokens}

class IntroductionRoles(Page):
    template_name = 'dimension/IntroductionRoles.html'

    def vars_for_template(self):
        return {'redeem_value': models.Constants.redeem_value,
        }

class AssignedDirections(Page):
    template_name = 'dimension/AssignedDirections.html'

    def vars_for_template(self):
        return {'rounds_per_game': models.Constants.rounds_per_game,
        }

class SellerInstructions(Page):
    template_name = 'dimension/SellerInstructions.html'

    def vars_for_template(self):
        return {'buyers_per_group': self.subsession.buyers_per_group,
        'num_other_sellers': self.subsession.sellers_per_group-1,
        'num_prices' : self.subsession.num_prices,
        'production_cost' : models.Constants.production_cost}

# class SellerQ1(Page):
#     template_name = 'dimension/GameInstructions2.html'

# class SellerQ2(Page):
#     template_name = 'dimension/GameInstructions2.html'

class BuyerInstructions(Page):
    template_name = 'dimension/BuyerInstructions.html'

class RoundSummaryExample(Page):
    template_name = 'dimension/RoundSummaryExample.html'

class Intro(Page):
    template_name = 'dimension/Intro.html'

class SetPrices(Page):
    template_name = 'dimension/SetPrices.html'
    form_model = models.Player

    def is_displayed(self):
        return self.player.role_int == 1

    def get_form_fields(self):
        return [
            'seller_price{}'.format(i)
            for i in range(self.subsession.num_prices)
        ]

    def vars_for_template(self):
        return {'num_prices': self.subsession.num_prices,
        'role' : self.player.role,
        'role_int' : self.player.role_int}

    def error_message(self, value):
        if sum(value.values()) > models.Constants.max_total_price:
            return "The sum of all prices must be less than or equal to {}".format(
                models.Constants.max_total_price)


class SelectSeller(Page):
    template_name = 'dimension/SelectSeller.html'
    form_model = models.Player
    form_fields = ('buyer_choice',)

    def is_displayed(self):
        return self.player.role_int == 2

    def vars_for_template(self):
        return {
            'sellers': enumerate(filter(
                lambda p: 1 == p.role_int,
                self.group.get_players()
            )),
        }

class SetPricesWaitPage(WaitPage):
    pass

class BuyerWaitPage(WaitPage):
    pass

    
class RoundSummary(Page):
    template_name = 'dimension/RoundSummary.html'

    def after_all_players_arrive(self):
        pass

    def vars_for_template(self):
        return {
        'sellers': enumerate(filter(
                lambda p: 1 == p.role_int,
                self.group.get_players()
            )), 'num_prices' : self.subsession.num_prices,
        'totalcosts' : self.player.total_cost(),
        'buyer_costs' : self.player.buyer_cost(),
        'number_sales' : self.player.number_sales(),
        'profits' : self.player.calculate_payoff()
        
        }

class RoundSummaryWait(WaitPage):
    wait_for_all_groups = True

page_sequence = [ 
    Begin,
    PRA,
    Introduction,
    IntroductionPayment,
    IntroductionRoles,
    AssignedDirections,
    SellerInstructions,
#    SellerQ1,
#    SellerQ2,
    BuyerInstructions,
    RoundSummaryExample,
    Intro,
    SetPrices,
    SetPricesWaitPage,
    SelectSeller,
    BuyerWaitPage,
    RoundSummary,
    RoundSummaryWait,
]

### All of these pages will go into a survey app
# SurveyExperience
# Numeracy
# RiskQ1,
# RiskQ2or3,
# RiskQ4
# Gender
# EndExperiment