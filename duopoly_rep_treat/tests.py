from otree.api import Currency as c, currency_range, Submission
from . import views
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        # Finding issue because game requires a manual advance from examiner, but don't know how to automate this advance. Maybe remove the page?
        if (self.subsession.round_number == 1):
          yield Submission(views.IntroductionSplash, check_html = False)
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

        if (self.subsession.round_number > Constants.num_rounds_practice + 1) and ((self.subsession.round_number - 1) % Constants.num_rounds_treatment == 0):
          yield(views.InstructionsNewTreatment)

        first = self.subsession.treatment_first_multiple or self.subsession.treatment_first_singular
        if (self.subsession.round_number !=1 and (self.subsession.block_new and first )):
          yield(views.InstructionsSeller)
          yield(views.InstructionsSellerPrices)
          yield(views.InstructionsBuyer)

        if ((self.subsession.round_number == Constants.num_rounds_practice + 1) or (self.subsession.block_new and not self.subsession.round_number == 1)):
          yield Submission(views.PracticeEnd, check_html = False)

        if (self.player.seller_bool):
          price_choice = random.randint(Constants.prodcost, Constants.maxprice)
          price_stdev = 1.0/(Constants.maxprice - Constants.prodcost)
          price_dims = [price_choice/(self.subsession.dims + 1)] * (self.subsession.dims + 1) 
          self.player.create_ask(total=price_choice, pricedims=price_dims, stdev=price_stdev)

          yield(views.ChoiceSeller, {"ask_total" : price_choice, "ask_stdev" : price_stdev})
        
        else:
          seller_choice = random.randint(1, Constants.sellers_per_group)
          yield(views.ChoiceBuyer, {"contract_seller_rolenum" : seller_choice})

        yield(views.RoundResults)