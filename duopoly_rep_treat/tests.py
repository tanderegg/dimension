from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == 1:
            yield (views.StartWait)
            yield (views.Begin)
            yield (views.PRA)
        if (self.subsession.round_number - models.Constants.num_rounds_practice) % model.Constants.num_rounds_treatment == 0:
	        yield (views.Introduction)
	        yield (views.IntroductionPayment)
	        yield (views.IntroductionRoles)
	        yield (views.AssignedDirections)
	        yield (views.SellerInstructions)
	        # Selecting random answer from choice set
	        choice = random.choice(['0 tokens', '{n} tokens'.format(self.Constants.redeem_value), 'It depends on the prices I set'])
	        yield (views.SellerQ1, {'quiz_q1': choice})
	        yield (views.SellerQ1Ans)
	        # Selecting random answer from choice set
	        choice = random.choice(['0 tokens', '{n} tokens'.format(self.Constants.redeem_value), 'It depends on the prices I set'])
	        yield (views.SellerQ2, {'quiz_q2': choice})
	        yield (views.SellerQ2Ans)
	        yield (views.BuyerInstructions)
	        yield (views.RoundSummaryExample)
        yield (views.Intro)
        yield (views.Instructions)

		# Seller Setting Prices	
        if self.player.roledesc == "Seller":
        	yield (views.SellerChoice, {'player.ask_total' : 400})
       	
       	def create_prices(self):

        # Buyer Choosing Seller
        if self.player.roledesc == "Buyer":
        	buyer_choice = random.choice([1,2])
        	yield (views.BuyerChoice, {'contract_seller_rolenum':})

        yield (views.RoundResults)

    def validate_play(self):
    	pass
