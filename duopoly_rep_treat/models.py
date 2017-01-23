from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.db.models import Model, ForeignKey
from statistics import pstdev

author = 'Dustin Beckett'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'duopoly_rep_treat'
    players_per_group = 4
    sellers_per_group = 2
    buyers_per_group = 2
    treatmentdims = [1, 8, 16]
    # treatmentorder = [1, 2, 3] # changes between sessions
    num_rounds_treatment = 1
    num_rounds_practice = 1
    num_rounds = num_rounds_treatment * len(treatmentdims) + num_rounds_practice
    num_players = 12
    prodcost = 100
    consbenefit = 800
    maxprice = 800
    minprice = 0


class Subsession(BaseSubsession):
    practiceround = models.BooleanField()
    realround = models.BooleanField()
    block = models.IntegerField()
    treatment = models.IntegerField()
    dims = models.IntegerField()

    def before_session_starts(self):

        # set treatment-level variables
        if self.round_number <= Constants.num_rounds_practice:
            # self.vars["practiceround"] = True
            self.practiceround = True
            self.realround = False
        else:
            # self.vars["practiceround"] = False
            self.practiceround = False
            self.realround = True

        # Assign treatment status and block
        if self.round_number <= Constants.num_rounds_treatment + Constants.num_rounds_practice:
            self.block = 1
        elif self.round_number <= 2 * Constants.num_rounds_treatment + Constants.num_rounds_practice:
            self.block = 2
        else:
            self.block = 3

        self.treatment = self.session.config["treatmentorder"][self.block - 1]
        self.dims = Constants.treatmentdims[self.treatment - 1]

        # Set player level variables
        # Randomize groups each round.
        self.group_randomly()

        for p in self.get_players():
            # set player roles
            p.set_role()

            # create player price dims
            p.generate_pricedims()


class Group(BaseGroup):
    # The group class is used to store market-level data
    mkt_bid_avg = models.FloatField()
    mkt_ask_min = models.IntegerField(default=800)
    mkt_ask_max = models.IntegerField(default=0)
    mkt_ask_spread = models.IntegerField()
    mkt_ask_stdev_min = models.FloatField()

    def set_marketvars(self):
        # this gets hit after all buyers and sellers have made their choices
        sellers = Player.objects.filter(group=self, roledesc="Seller")
        buyers = Player.objects.filter(group=self, roledesc="Buyer")

        # Seller data
        for buyer in buyers:
            # adjust numsold for sellers
            self.get_player_by_role("S" + str(buyer.contract_seller_rolenum)).numsold += 1
            # buyer profit

        for seller in sellers:
            seller.profit = seller.numsold * (seller.ask_total - Constants.prodcost)

        # Market data
        self.mkt_ask_min = min([ s.ask_total for s in sellers ])
        self.mkt_ask_max = max([ s.ask_total for s in sellers ])
        self.mkt_ask_spread = self.mkt_ask_max - self.mkt_ask_min
        self.mkt_bid_avg = float(sum([ int(b.bid_total) for b in buyers ])) / len(buyers)
        self.mkt_ask_stdev_min = min([ s.ask_stdev for s in sellers ])





class Player(BasePlayer):
    # Both
    rolenum = models.IntegerField()
    roledesc = models.CharField()
    profit = models.IntegerField()
    profit_interim = models.IntegerField()

    # Seller
    ask_total = models.IntegerField(min=Constants.minprice, max=Constants.maxprice)
    ask_stdev = models.FloatField()
    numsold = models.IntegerField(default=0)

    # Buyer
    bid_total = models.IntegerField(min=Constants.minprice, max=Constants.maxprice)
    contract_seller_rolenum = models.IntegerField(
        choices=[(1, "Seller 1"), (2, "Seller 2")],
        widget=widgets.RadioSelect()
    )
    mistake_bool = models.IntegerField()
    mistake_size = models.IntegerField(default=0)
    other_seller_ask_total = models.IntegerField()
    other_seller_ask_stdev = models.FloatField()

    # wait page game
    gamewait_numcorrect = models.IntegerField()# , widget=widgets.HiddenInput()# TextInput()) # attrs={"type":"hidden"}


    def set_prices_buyer(self):
        """ Use buyer's seller selection to fill in other attributes for the buyer """
        rolenum_other = [ rn for rn in [1,2] if rn != self.contract_seller_rolenum][0]
        seller = self.group.get_player_by_role("S" + str(self.contract_seller_rolenum))
        seller_other = self.group.get_player_by_role("S" + str(rolenum_other))

        self.bid_total = seller.ask_total
        self.other_seller_ask_total = seller_other.ask_total
        self.mistake_size = max(0, self.bid_total - self.other_seller_ask_total)
        self.mistake_bool = 0 if self.mistake_size <= 0 else 1

        other_seller_ask_stddev = pstdev([ int(pd.value) for pd in seller_other.pricedim_set.all() ])

        for pd in self.pricedim_set.all():
            pd.value = seller.pricedim_set.get(dimnum=pd.dimnum).value
            pd.save()

        # profit
        self.profit = Constants.consbenefit - self.bid_total


    def set_prices_seller(self, submitted_data):
        """ Get prices from seller form and save the values.
            Seller profit and numsold (vars that depend on buyer actions) set in group.set_marketvars
        """
        # this filter doesn't seem necessary
        # pricedims = self.player.pricedim_set.filter(player__exact=self.player)
        pricedims = self.pricedim_set.all()

        for pd in pricedims:
            pd.value = submitted_data["dim_{}".format(pd.dimnum)]
            pd.save()

        self.ask_stdev = pstdev([int(pd.value) for pd in pricedims])

    def generate_pricedims(self):
        # if self.subsession.treatment:
        # otree trying to assess subsession.treatment at build time, so this if just skips that
        for i in range(self.subsession.dims):
            pd = self.pricedim_set.create(dimnum = i + 1)
            pd.save()

    def set_role(self):
        # since we've randomized player ids in groups in the subsession class, we can assign role via id_in_group here
        if self.id_in_group == 1:
            self.rolenum = 1
            self.roledesc = "Seller"
        elif self.id_in_group == 2:
            self.rolenum = 2
            self.roledesc = "Seller"
        elif self.id_in_group == 3:
            self.rolenum = 1
            self.roledesc = "Buyer"
        else:
            self.rolenum = 2
            self.roledesc = "Buyer"

    def role(self):
        return self.roledesc[0] + str(self.rolenum)

class PriceDim(Model):   # our custom model inherits from Django's base class "Model"

    value = models.IntegerField()
    dimnum = models.IntegerField()

    player = ForeignKey(Player)    # creates 1:m relation -> this decision was made by a certain player