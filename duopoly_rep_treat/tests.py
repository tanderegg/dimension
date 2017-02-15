from otree.api import Currency as c, currency_range, Submission
from . import views
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):


    # NOTE: To turn on browser bots, go to settings.py and set field 'use_browser_bots' to true for both survey and duopoly_rep_treat
    def play_round(self):
        # Going through instruction pages in beginning of the game
        if (self.subsession.round_number == 1):
          yield Submission(views.IntroductionSplash, check_html = False) # Different syntax for splash pages (don't have 'next' buttons)
          yield(views.IntroductionPRA)
          yield(views.InstructionsBasics)
          yield(views.InstructionsPayment)
          yield(views.InstructionsRoles)
          yield(views.InstructionsSeller)
          yield(views.InstructionsSellerPrices)
          yield(views.InstructionsSellerQ1)
          yield(views.InstructionsSellerQ1Ans)
          yield(views.InstructionsSellerQ2)
          yield(views.InstructionsSellerQ2Ans)
          yield(views.InstructionsBuyer)
          yield(views.InstructionsRoundResults)
          yield(views.InstructionsWaitGame)
          yield(views.InstructionsCleanUp)
          yield(views.PracticeBegin)  

        # New treatment page only comes in between two treatments for paid rounds
        if (self.subsession.round_number > Constants.num_rounds_practice + 1) and ((self.subsession.round_number - 1) % Constants.num_rounds_treatment == 0):
          yield(views.InstructionsNewTreatment)

        # Reviews instructions once after first round
        first = self.subsession.treatment_first_multiple or self.subsession.treatment_first_singular
        if (self.subsession.round_number != 1 and (self.subsession.block_new and first)):
          yield(views.InstructionsSeller)
          yield(views.InstructionsSellerPrices)
          yield(views.InstructionsBuyer)

        # Pass through splash screen between practice and paid rounds
        if ((self.subsession.round_number == Constants.num_rounds_practice + 1) or (self.subsession.block_new and not self.subsession.round_number == 1)):
          yield Submission(views.PracticeEnd, check_html = False)

        # Set and submit ask prices if participant is a seller this round
        if (self.player.seller_bool):
          price_choice = random.randint(Constants.prodcost, Constants.maxprice)
          price_dims = [price_choice/(self.subsession.dims + 1)] * (self.subsession.dims + 1)
          price_stdev = 0
          self.player.create_ask(total=price_choice, pricedims=price_dims)

          yield(views.ChoiceSeller, {"ask_total" : price_choice, "ask_stdev" : price_stdev})
        
        # Randomly choose seller from available choices
        else:
          seller_choice = random.randint(1, Constants.sellers_per_group)
          yield(views.ChoiceBuyer, {"contract_seller_rolenum" : seller_choice})

        yield(views.RoundResults)