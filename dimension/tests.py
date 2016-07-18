# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        if self.subsession.round_number == 1:
            self.submit(views.Begin)
            self.submit(views.PRA)

        self.submit(views.Introduction)
        self.submit(views.IntroductionPayment)
        self.submit(views.IntroductionRoles)
        self.submit(views.AssignedDirections)
        self.submit(views.SellerInstructions)
        self.submit(views.BuyerInstructions)
        self.submit(views.RoundSummaryExample)
        self.submit(views.Intro)

        if self.player.role_int == 1:
            if self.subsession.num_prices == 1:
                price = random.randint(0,400)
                self.submit(views.SetPrices, {'seller_price0': price})
            elif self.subsession.num_prices==4:
                prices = [random.randint(0,400/2) for x in xrange(4)]
                self.submit(views.SetPrices, {'seller_price0' : prices[0],
                    'seller_price1' : prices[1], 'seller_price2' : prices[2],
                    'seller_price3' : prices[3]})
            else:
                prices = [random.randint(0,400/4) for x in xrange(8)]
                self.submit(views.SetPrices, {'seller_price0' : prices[0],
                    'seller_price1' : prices[1], 'seller_price2' : prices[2],
                    'seller_price3' : prices[3], 'seller_price4' : prices[4],
                    'seller_price5' : prices[5], 'seller_price6' : prices[6],
                    'seller_price7' : prices[7]})
        else:
            choice = random.choice([0,1])
            self.submit(views.SelectSeller, {'buyer_choice': choice})

        self.submit(views.RoundSummary)

                
        
    def validate_play(self):
        pass

