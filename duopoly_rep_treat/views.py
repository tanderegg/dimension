from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, PriceDim, Ask, Player, Subsession, Group, BaseSubsession
from django.http import JsonResponse, HttpResponse
from statistics import pstdev
from django.shortcuts import render
from . import utils, export
from otree.models.session import Session

class Begin(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class PRA(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions


class Introduction(Page):

    def vars_for_template(self):
        return {'num_rounds': Constants.num_rounds_treatment,
        'num_games' : self.subsession.num_dims}

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class IntroductionPayment(Page):

    def vars_for_template(self):
        return {'redeem_value': Constants.consbenefit,
            'cents_per_token': self.session.config["real_world_currency_per_point"],#self.subsession.currency_per_point,
            'tokens_per_dollar': int(100./float(self.session.config["real_world_currency_per_point"])),
            'starting_tokens' : Constants.starting_tokens,
            'total_rounds': Constants.num_treatments*Constants.num_rounds_treatment + Constants.num_rounds_practice,
            'showup': self.session.config['participation_fee'],
        }

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class IntroductionRoles(Page):

    def vars_for_template(self):
        return {#'redeem_value': Constants.consbenefit,
                'num_groups': int(Constants.num_players/Constants.players_per_group),
        }

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class NewTreatmentInstructions(Page):

    def is_displayed(self):
        return not self.subsession.round_number == 1 and self.subsession.block_new and Constants.show_instructions

class SellerInstructions(Page):

    def vars_for_template(self):
        return {'buyers_per_group': Constants.buyers_per_group,
            'num_other_sellers': Constants.sellers_per_group-1,
            # 'num_prices' : self.subsession.dims,
            'production_cost' : Constants.prodcost,
            'price_dims': range(1, self.subsession.dims + 1)
                }

    def is_displayed(self):
        # want to display these instructions to people on their first round or if its the first time they see either
        # a 1 dim case or a multiple dim case (so, basically, a complex way of saying "BLOCK 2").
        first = self.subsession.treatment_first_multiple or self.subsession.treatment_first_singular
        return Constants.show_instructions and (self.subsession.round_number==1 or (self.subsession.block_new and first ))

class SellerInstructionsPrices(Page):

    def vars_for_template(self):
        return {
            'price_dims': range(1, self.subsession.dims + 1)
                }
    def is_displayed(self):
        # want to display these instructions to people on their first round or if its the first time they see either
        # a 1 dim case or a multiple dim case (so, basically, a complex way of saying "BLOCK 2").
        first = self.subsession.treatment_first_multiple or self.subsession.treatment_first_singular
        return Constants.show_instructions and (self.subsession.round_number == 1 or (self.subsession.block_new and first))

class SellerQ1(Page):
    form_model = models.Player
    form_fields = ['quiz_q1']

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class SellerQ1Ans(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

    def vars_for_template(self):
        return {'correct_answer' : '0 tokens'}

class SellerQ2(Page):
    form_model = models.Player
    form_fields = ['quiz_q2']

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class SellerQ2Ans(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

    def vars_for_template(self):
        return {'correct_answer' : 'It depends on the prices I set'}

class BuyerInstructions(Page):

    def is_displayed(self):
        # want to display these instructions to people on their first round or if its the first time they see either
        # a 1 dim case or a multiple dim case (so, basically, a complex way of saying "BLOCK 2").
        first = self.subsession.treatment_first_multiple or self.subsession.treatment_first_singular
        return Constants.show_instructions and (
            self.subsession.round_number == 1 or (self.subsession.block_new and first))

    def vars_for_template(self):

        return{
            "prices": utils.get_example_prices(self.subsession.dims),
        }

class RoundSummaryExample(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

    def vars_for_template(self):
        player = Player(roledesc="Seller", payoff=225, ask_total=325, numsold=1, rolenum=1)

        return{
            "player": player,
            "subtotal": 225,
            "prices": utils.get_example_prices(self.subsession.dims),
            "s1_ask_total": 325,
            "s2_ask_total": 375,
            "b1_seller": 1,
            "b2_seller": 2,
        }

class WaitGameExample(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class InstructionsCleanUp(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1 and Constants.show_instructions

class PracticeBegin(Page):

    def is_displayed(self):
        return self.subsession.round_number==1 and Constants.num_rounds_practice > 0

    def vars_for_template(self):
        otherrole = [role for role in ["Buyer", "Seller"] if role != self.player.roledesc][0]
        return {
            "otherrole": otherrole,
        }

class PracticeEnd(Page):
    def is_displayed(self):
        # return self.subsession.round_number == Constants.num_rounds_practice + 1
        # want to display these instructions to people on their first PAID round or if its the first round in a new block
        # first = self.subsession.treatment_first_multiple or self.subsession.treatment_first_singular
        return self.subsession.round_number == Constants.num_rounds_practice + 1 or \
               (self.subsession.block_new and not self.subsession.round_number == 1)


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
    form_fields = ['ask_total', 'ask_stdev']


    def is_displayed(self):
        return self.player.roledesc == "Seller"

    def vars_for_template(self):
        round_temp = (self.subsession.round_number - Constants.num_rounds_practice) % Constants.num_rounds_treatment
        round = round_temp if round_temp > 0 else Constants.num_rounds_treatment
        return{
            #'price_dims': self.player.pricedim_set.all()
            "price_dims": range(1, self.subsession.dims+1),
            "round": round
        }

    def before_next_page(self):
        """
            If dims==1 then we need to make and aks object. For the multiple dims case, this is handled when the user
            presses the "distrubute" button or manually edits one of the dim fields.  The dim fields do not exist
            when dims==1.
        """
        if self.subsession.dims == 1:
            player = self.player
            player.create_ask(player.ask_total, pricedims=[player.ask_total], auto=None, manual=None, stdev=0)




# BUYER PAGE

class BuyerChoice(Page):

    form_model = models.Player
    form_fields = ['contract_seller_rolenum']

    def is_displayed(self):
        return self.player.roledesc == "Buyer"

    def vars_for_template(self):
        round_temp = (self.subsession.round_number - Constants.num_rounds_practice) % Constants.num_rounds_treatment
        round = round_temp if round_temp > 0 else Constants.num_rounds_treatment
        # if self.subsession.dims > 1:
        prices = zip(range(1, self.subsession.dims + 1),
            [pd.value for pd in self.group.get_player_by_role("S1").get_ask().pricedim_set.all()],
            [pd.value for pd in self.group.get_player_by_role("S2").get_ask().pricedim_set.all()])
        # else:
        #     prices = [[self.group.get_player_by_role("S1").ask_total, self.group.get_player_by_role("S2").ask_total]]
        return {
            "prices": prices,
            "round": round
        }

    def before_next_page(self):
        """ Create bid object.  Set buyer price attributes """
        seller = self.group.get_player_by_role("S" + str(self.player.contract_seller_rolenum))
        ask = seller.get_ask()
        pricedims = [pd.value for pd in ask.pricedim_set.all()]

        bid = self.player.create_bid(ask.total, pricedims)

        self.group.create_contract(bid=bid, ask=ask)
        self.player.set_buyer_data()





# WAIT PAGES

class StartWait(WaitPage):
    # This makes sures everyone has cleared the results page before the next round begins
    wait_for_all_groups = True
    title_text = "Waiting for Other Participants"
    body_text = "Please wait for other participants."


class StartMatchWait(WaitPage):
    # This makes sures everyone has cleared the instructions pages before the next round begins
    wait_for_all_groups = True
    title_text = "Waiting for Other Participants"
    body_text = "Please wait for other participants."


class WaitSellersForSellers(WaitPage):
    wait_for_all_groups = True
    title_text = "Waiting for Sellers"
    body_text = "You are a buyer. Please wait for the sellers to set their prices."

    def is_displayed(self):
        return self.player.roledesc == "Buyer"


class WaitBuyersForSellers(WaitPage):
    wait_for_all_groups = True
    title_text = "Waiting for Sellers"
    body_text = "Please wait for the other sellers to set their prices."

    def is_displayed(self):
        return self.player.roledesc == "Seller"

    def after_all_players_arrive(self):
        # When here, sellers have all entered their prices
        # self.group.set_marketvars_seller()
        pass

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
            "prices": zip(range(1, self.subsession.dims + 1),
                             [pd.value for pd in self.group.get_player_by_role("S1").get_ask().pricedim_set.all() ],
                             [pd.value for pd in self.group.get_player_by_role("S2").get_ask().pricedim_set.all()] ),
            "s1_ask_total": self.group.get_player_by_role("S1").ask_total,
            "s2_ask_total": self.group.get_player_by_role("S2").ask_total,
            "b1_seller": self.group.get_player_by_role("B1").contract_seller_rolenum,
            "b2_seller": self.group.get_player_by_role("B2").contract_seller_rolenum,
            "subtotal": self.player.ask_total - Constants.prodcost if self.player.ask_total != None else 0
        }



# AJAX VIEWS
# Seller Asks
def AutoPricedims(request):

    pricejson = utils.get_autopricedims(
        ask_total=int(round(float(request.POST["ask_total"]))), numdims=int(round(float(request.POST["numdims"]))))

    if not request.POST["example"] == "True":
        # If this is being called from the instructions screen, we skip adding a row
        player = utils.get_player_from_request(request)

        ask = player.create_ask(total=pricejson["ask_total"], auto=True, manual=False, stdev=pricejson["ask_stdev"],
                            pricedims=pricejson["pricedims"])

    print(pricejson)
    return JsonResponse(pricejson)

def ManualPricedims(request):

    result = request.POST.dict()

    pricedims_raw = result["pricedims"].split(",")
    pricedims = [None if pd=="" else int(round(float(pd))) for pd in pricedims_raw]
    total = sum([0 if pd=="" else int(round(float(pd))) for pd in pricedims_raw])

    if not request.POST["example"] == "True":
        # If this is being called from the instructions screen, we skip adding a row
        player = utils.get_player_from_request(request)

        ask = player.create_ask(total=total, auto=False, manual=True, pricedims=pricedims)
        ask.stdev = pstdev([int(pd.value) for pd in ask.pricedim_set.all() if not pd.value==None ])
        ask.save()

        return JsonResponse({"pricedims": pricedims, "ask_total": ask.total, "ask_stdev": ask.stdev})
    else:
        # If here, this is an example request from the instructions screen
        return JsonResponse({"pricedims": pricedims, "ask_total": total, "ask_stdev": 0})





# Wait Page Game
def GameWaitIterCorrect(request):

    player = utils.get_player_from_request(request)
    player.gamewait_numcorrect += 1
    player.save()

    return JsonResponse({"gamewait_numcorrect": player.gamewait_numcorrect})



# Data Views

def ViewData(request):
    return render(request, 'duopoly_rep_treat/data.html', {"session_code": Session.objects.last().code})


def AskDataView(request):
    (headers, body) = export.export_asks()

    context = {"title": "Seller Ask Data", "headers": headers, "body": body}
    return render(request, 'duopoly_rep_treat/DataView.html', context)

def AskDataDownload(request):

    headers, body = export.export_asks()
    return export.export_csv("AskData", headers, body)


def ContractDataView(request):
    (headers, body) = export.export_contracts()

    context = {"title": "Contracts Data", "headers": headers, "body": body}
    return render(request, 'duopoly_rep_treat/DataView.html', context)

def ContractDataDownload(request):

    headers, body = export.export_contracts()
    return export.export_csv("ContractData", headers, body)


def MarketDataView(request):
    headers, body = export.export_marketdata()
    context = {"title": "Market Data", "headers": headers, "body": body}

    return render(request, 'duopoly_rep_treat/DataView.html', context)

def MarketDataDownload(request):

    headers, body = export.export_marketdata()
    return export.export_csv("MarketData", headers, body)


def SurveyDataView(request):
    headers, body = export.export_surveydata()
    context = {"title": "Survey Data", "headers": headers, "body": body}

    return render(request, 'duopoly_rep_treat/DataView.html', context)

def SurveyDataDownload(request):

    headers, body = export.export_surveydata()
    return export.export_csv("SurveyData", headers, body)


def CombinedDataView(request):
    headers, body = export.export_combineddata()
    context = {"title": "Combined Data", "headers": headers, "body": body}

    return render(request, 'duopoly_rep_treat/DataView.html', context)

def CombinedDataDownload(request):

    headers, body = export.export_combineddata()
    return export.export_csv("CombinedData", headers, body)


page_sequence = [
    StartWait,
    Begin,
    PRA,
    Introduction,
    IntroductionPayment,
    IntroductionRoles,
    NewTreatmentInstructions,
    SellerInstructions,
    SellerInstructionsPrices,
    SellerQ1,
    SellerQ1Ans,
    SellerQ2,
    SellerQ2Ans,
    BuyerInstructions,
    RoundSummaryExample,
    WaitGameExample,
    InstructionsCleanUp,
    StartMatchWait,
    # AssignedDirections,
    PracticeBegin,
    PracticeEnd,
    # Instructions,
    SellerChoice,
    WaitSellersForSellers,  # for buyers while they wait for sellers # split in tow
    WaitBuyersForSellers,  # for buyers while they wait for sellers # split in tow
    BuyerChoice,
    WaitGame, # both buyers and sellers go here while waiting for buyers
    WaitRoundResults,
    RoundResults
]
