from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, PriceDim, Ask, Player, Subsession, Group
from django.http import JsonResponse, HttpResponse
from statistics import pstdev
from django.shortcuts import render
import csv
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
    form_fields = ['ask_total', 'ask_stdev']


    def is_displayed(self):
        return self.player.roledesc == "Seller"

    def vars_for_template(self):
        return{
            #'price_dims': self.player.pricedim_set.all()
            "price_dims": range(1, self.subsession.dims+1)
        }

    def before_next_page(self):
        """ Set the seller price attributes """
        # get the raw submitted data as dict
        # submitted_data = self.form.data
        # self.player.set_prices_seller(submitted_data)
        # self.player.set_prices_seller()




# BUYER PAGE

class BuyerChoice(Page):

    form_model = models.Player
    form_fields = ['contract_seller_rolenum']

    def is_displayed(self):
        return self.player.roledesc == "Buyer"

    def vars_for_template(self):
        return {
            "pricedims": zip(range(1, self.subsession.dims + 1),
                             [ pd.value for pd in self.group.get_player_by_role("S1").get_ask().pricedim_set.all() ],
                             [pd.value for pd in self.group.get_player_by_role("S2").get_ask().pricedim_set.all()] ),
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
                             [pd.value for pd in self.group.get_player_by_role("S1").get_ask().pricedim_set.all() ],
                             [pd.value for pd in self.group.get_player_by_role("S2").get_ask().pricedim_set.all()] ),
            "s1_ask_total": self.group.get_player_by_role("S1").ask_total,
            "s2_ask_total": self.group.get_player_by_role("S2").ask_total,
            "b1_seller": self.group.get_player_by_role("B1").contract_seller_rolenum,
            "b2_seller": self.group.get_player_by_role("B2").contract_seller_rolenum,
            "subtotal": self.player.ask_total - Constants.prodcost if self.player.ask_total != None else 0
        }



# AJAX VIEWS

def AutoPricedims(request):

    pricejson = utils.get_autopricedims(
        ask_total=int(round(float(request.POST["ask_total"]))), numdims=int(round(float(request.POST["numdims"]))))

    subsession = Subsession.objects.get(id=request.POST["subsession_id"])
    group = Group.objects.get(id=request.POST["group_id"], subsession=subsession)
    player = Player.objects.get(id_in_group=int(request.POST["player_id_in_group"]), group=group)

    ask = player.create_ask(total=pricejson["ask_total"], auto=True, manual=False, stdev=pricejson["ask_stdev"],
                            pricedims=pricejson["pricedims"])

    print(pricejson)
    return JsonResponse(pricejson)


def ManualPricedims(request):

    result = request.POST.dict()

    pricedims_raw = result["pricedims"].split(",")
    pricedims = [None if pd=="" else int(round(float(pd))) for pd in pricedims_raw]
    total = sum([0 if pd=="" else int(round(float(pd))) for pd in pricedims_raw])

    subsession = Subsession.objects.get(id=result["subsession_id"])
    group = Group.objects.get(id=result["group_id"], subsession=subsession)
    player = Player.objects.get(id_in_group=int(result["player_id_in_group"]), group=group)

    ask = player.create_ask(total=total, auto=False, manual=True, pricedims=pricedims)
    ask.stdev = pstdev([int(pd.value) for pd in ask.pricedim_set.all() if not pd.value==None ])
    ask.save()

    return JsonResponse({"pricedims": pricedims, "ask_total": ask.total, "ask_stdev": ask.stdev})



# Data Views

def ViewData(request):
    return render(request, 'duopoly_rep_treat/data.html')

def get_filename(suffix):
    subsession = Subsession.objects.last()
    if subsession == None:
        return ([], [])
    date = subsession.session.config["date"]
    time = subsession.session.config["time"]
    filename = "{}_{}_{}.csv".format(date, time, suffix)

    return filename

def AskDataDownload(request):
    # Create the HttpResponse object with the appropriate CSV header.
    filename = get_filename("askdata")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    (headers, body) = utils.export_asks()

    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(body)

    return response


def AskDataView(request):
    (headers, body) = utils.export_asks()

    context = {"title": "Seller Ask Data", "headers": headers, "body": body}
    return render(request, 'duopoly_rep_treat/DataView.html', context)


def MarketDataView(request):
    headers, body = utils.export_marketdata()
    context = {"title": "Market Data", "headers": headers, "body": body}

    return render(request, 'duopoly_rep_treat/DataView.html', context)


def MarketDataDownload(request):
    filename = get_filename("marketdata")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    (headers, body) = utils.export_marketdata()

    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(body)

    return response

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
