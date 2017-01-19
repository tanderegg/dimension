from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, PriceDim
# from django.views import View
from django.http import JsonResponse

from . import utils

class Instructions(Page):
    def is_displayed(self):
        # want to display instructions before the first practice round, and before the first real round in all OTHER
        #   treatments
        if self.round_number == 1:
            return True
        elif self.round_number <= Constants.num_rounds_practice + 1:
            # don't want instructions appearing after the practice rounds
            return False
        elif (self.round_number - Constants.num_rounds_practice) % Constants.num_rounds_treatment == 1:
            return True
        else:
            return False


# SELLER PAGE

class SellerChoice(Page):

    form_model = models.Player
    form_fields = ['ask_total']

    def is_displayed(self):
        return self.player.roledesc == "Seller"

    def vars_for_template(self):
        return{
            'price_dims': self.player.pricedim_set.all()
        }

    def before_next_page(self):
        """ Set the seller price attributes """
        # get the raw submitted data as dict
        submitted_data = self.form.data
        self.player.set_prices_seller(submitted_data)




# BUYER PAGE

class BuyerChoice(Page):

    form_model = models.Player
    form_fields = ['contract_seller_rolenum']

    def is_displayed(self):
        return self.player.roledesc == "Buyer"

    def vars_for_template(self):
        return {
            "pricedims": zip(range(1, self.subsession.dims + 1),
                             [ pd.value for pd in self.group.get_player_by_role("S1").pricedim_set.all() ],
                             [pd.value for pd in self.group.get_player_by_role("S2").pricedim_set.all()] ),
        }

    def before_next_page(self):
        """ Set buyer price attributes """
        self.player.set_prices_buyer()




# WAIT PAGES

class StartWait(WaitPage):
    # This makes sures everyone has cleared the results page before the next round begins
    wait_for_all_groups = True
    title_text = "Waiting for Other Players"
    body_text = "Please wait while your group is created."


class WaitSellersForSellers(WaitPage):
    wait_for_all_groups = True
    title_text = "Waiting for Sellers"
    body_text = "Please wait for the sellers to set prices."

    def is_displayed(self):
        return self.player.roledesc == "Buyer"


class WaitBuyersForSellers(WaitPage):
    wait_for_all_groups = True
    title_text = "Waiting for Sellers"
    body_text = "Please wait for the other sellers to set prices."

    def is_displayed(self):
        return self.player.roledesc == "Seller"

    def after_all_players_arrive(self):
        # When here, sellers have all entered their prices
        self.group.set_marketvars_seller()


# class WaitSellersForBuyers(WaitPage):
#     wait_for_all_groups = True
#     title_text = "Waiting for Buyers"
#     body_text = "Please wait for the buyers to make their selections."
#
#     def after_all_players_arrive(self):
#         pass
#     def is_displayed(self):
#         return self.player.roledesc == "Seller"


class WaitGame(WaitPage):
    template_name = 'duopoly_rep_treat/GameWait.html'
    wait_for_all_groups = True

    form_model = models.Player
    form_fields = ['gamewait_numcorrect']

    def after_all_players_arrive(self):
        pass


class WaitRoundResults(WaitPage):
    # This is just a trigger to calculate the payoffs and market variables before the results page

    def after_all_players_arrive(self):
        # When here, buyers and sellers have made their choices
        self.group.set_marketvars()


# RESULTS

class RoundResults(Page):
    def vars_for_template(self):
        return {
            "pricedims": zip(range(1, self.subsession.dims + 1),
                             [ pd.value for pd in self.group.get_player_by_role("S1").pricedim_set.all() ],
                             [pd.value for pd in self.group.get_player_by_role("S2").pricedim_set.all()] ),
            "s1_ask_total": self.group.get_player_by_role("S1").ask_total,
            "s2_ask_total": self.group.get_player_by_role("S2").ask_total,
            "b1_seller": self.group.get_player_by_role("B1").contract_seller_rolenum,
            "b2_seller": self.group.get_player_by_role("B2").contract_seller_rolenum,
            "subtotal": self.player.ask_total - Constants.prodcost if self.player.ask_total != None else 0
        }



# AJAX VIEWS

def AutoPricedims(request):

    print(request.POST)
    print(request.POST["ask_total"])

    pricedims = utils.get_autopricedims(int(request.POST["ask_total"]), int(request.POST["numdims"]))

    # def post(self, request, *args, ):
    # print("in view post")
    # print(request.POST)
    # for i in request.POST:
    #     print(i)
    # print("hmm")

    # pretty sure this is not what we want.  even if http is right, we need something special for post
    print(pricedims)
    return JsonResponse({'pricedims': pricedims})


page_sequence = [
    StartWait,
    Instructions,
    SellerChoice,
    WaitSellersForSellers,  # for buyers while they wait for sellers # split in tow
    WaitBuyersForSellers,  # for buyers while they wait for sellers # split in tow
    BuyerChoice,
    #WaitSellersForBuyers, # for sellers while they wait for buyers # remove
    WaitGame, # both buyers and sellers go here while waiting for buyers
    WaitRoundResults,
    RoundResults
]
