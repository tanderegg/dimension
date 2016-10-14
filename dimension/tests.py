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
        # Selecting answers that 
        choice = random.choice(['0 tokens', '{n} tokens'.format(self.Constants.redeem_value), 'It depends on the prices I set'])
        self.submit(views.SellerQ1, {'quiz_q1': choice})
        self.submit(views.SellerQ1Ans)
        self.submit(views.SellerQ2, {'quiz_q2': choice})
        self.submit(views.SellerQ2Ans)
        self.submit(views.BuyerInstructions)
        self.submit(views.RoundSummaryExample)
        self.submit(views.Intro)

        # Seller setting prices
        if self.player.role_int == 1:
            if self.subsession.num_prices == 1:
                price = random.randint(0,400)
                self.submit(views.SetPrices, {'seller_price0': price})
            elif self.subsession.num_prices==8:
                prices = [random.randint(0,100) for x in range(self.subsession.num_prices)]
                self.submit(views.SetPrices, {'seller_price0' : prices[0],
                    'seller_price1' : prices[1], 'seller_price2' : prices[2],
                    'seller_price3' : prices[3], 'seller_price4' : prices[4],
                    'seller_price5' : prices[5], 'seller_price6' : prices[6],
                    'seller_price7' : prices[7]})
            else:
                prices = [random.randint(0,50) for x in range(self.subsession.num_prices)]
                self.submit(views.SetPrices, {'seller_price0' : prices[0],
                    'seller_price1' : prices[1], 'seller_price2' : prices[2],
                    'seller_price3' : prices[3], 'seller_price4' : prices[4],
                    'seller_price5' : prices[5], 'seller_price6' : prices[6],
                    'seller_price7' : prices[7],'seller_price8' : prices[8],
                    'seller_price9' : prices[9], 'seller_price10' : prices[10],
                    'seller_price11' : prices[11], 'seller_price12' : prices[12],
                    'seller_price13' : prices[13], 'seller_price14' : prices[14],
                    'seller_price15' : prices[15]})
                
        # Buyer selecting a seller randomly
        else:
            choice = random.choice([0,1])
            self.submit(views.SelectSeller, {'buyer_choice': choice})

        self.submit(views.RoundSummary)

                
        
    def validate_play(self):
        pass

