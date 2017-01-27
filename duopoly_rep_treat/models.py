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
    starting_tokens = 500
    # For convenience of testing the experience of players
    show_instructions = True


class Subsession(BaseSubsession):
    practiceround = models.BooleanField()
    realround = models.BooleanField()
    block = models.IntegerField()
    treatment = models.IntegerField()
    dims = models.IntegerField()
    num_dims = models.IntegerField()
    currency_per_point = models.DecimalField(decimal_places = 2, max_digits = 6)

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
        self.num_dims = len(self.session.config["treatmentorder"])
        self.currency_per_point = self.session.config["real_world_currency_per_point"]

        # Set player level variables
        # Randomize groups each round.
        self.group_randomly()

        for p in self.get_players():
            # set player roles
            p.set_role()

            # create player price dims
            # p.generate_pricedims()


class Group(BaseGroup):
    # The group class is used to store market-level data
    mkt_bid_avg = models.FloatField()
    mkt_ask_min = models.IntegerField()
    mkt_ask_max = models.IntegerField()
    mkt_ask_spread = models.IntegerField()
    mkt_ask_stdev_min = models.FloatField()

    def create_contract(self, bid, ask):
        contract = Contract(bid=bid, ask=ask, group=self)
        contract.save()

    def set_marketvars(self):
        # this gets hit after all buyers and sellers have made their choices
        # sellers = Player.objects.filter(group=self, roledesc="Seller")
        # buyers = Player.objects.filter(group=self, roledesc="Buyer")

        contracts = Contract.objects.filter(group=self)

        print("contracts")
        print(contracts)
        print("ask totals")
        print([c.ask.total for c in contracts])

        # Player data
        for contract in contracts:
            seller = contract.ask.player
            buyer = contract.bid.player

            seller.numsold += 1
            seller.payoff += seller.ask_total - Constants.prodcost

            buyer.payoff = Constants.consbenefit - buyer.bid_total

        for player in self.get_players():
            player.payoff_interim = player.payoff + player.participant.payoff

        # Market data
        self.mkt_ask_min = min([c.ask.total for c in contracts])
        self.mkt_ask_max = max([c.ask.total for c in contracts])
        self.mkt_ask_spread = self.mkt_ask_max - self.mkt_ask_min
        self.mkt_bid_avg = float(sum([c.bid.total for c in contracts])) / len(contracts)
        self.mkt_ask_stdev_min = min([c.ask.stdev for c in contracts])






class Player(BasePlayer):
    # Both
    rolenum = models.IntegerField()
    roledesc = models.CharField()

    # Instruction Questions
    quiz_q1 = models.CharField(
        choices = ['0 tokens', '{} tokens'.format(Constants.consbenefit), 'It depends on the prices I set'],
        blank = True,
        widget = widgets.RadioSelect(),
        verbose_name = "How many tokens will you receive if you don't sell an object?")

    quiz_q2 = models.CharField(
        choices = ['0 tokens', '{} tokens'.format(Constants.consbenefit), 'It depends on the prices I set'],
        blank = True,
        widget = widgets.RadioSelect(),
        verbose_name = 'How many tokens will you receive if you sell an object?')
    
    # profit = models.IntegerField(default=0) # use built-in payoff field
    # profit_interim = models.IntegerField(default=0)
    payoff_interim = models.CurrencyField(default=0)
    buyer_bool = models.BooleanField()
    seller_bool = models.BooleanField()

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
    gamewait_numcorrect = models.IntegerField(default=0)# , widget=widgets.HiddenInput()# TextInput()) # attrs={"type":"hidden"}

    def create_bid(self, bid_total, pricedims):
        """ Creates a bid row associated with the buyer after the buyer makes his/her choice """

        bid = Bid(player=self, total=bid_total)
        bid.save()
        bid.set_pricedims(pricedims)

        return bid

    def create_ask(self, total, pricedims=None, auto=None, manual=None, stdev=None):
        """
            Creates an ask row associated with the seller
            :param total: integer total price
            :param pricedims: optional. list of integer pricedims
            :return: ask object
        """
        ask = Ask(player=self, total=total, auto=auto, manual=manual, stdev=stdev)
        ask.save()
        # if pricedims == None:
        #ask.generate_pricedims()
        # else:
        ask.set_pricedims(pricedims)

        return ask

    def get_ask(self):
        """ Get the latest ask row associated with this player """
        ask = self.ask_set.order_by("id").last()
        return ask

    def get_ask_pricedims(self):
        ask = self.get_ask()
        if ask == None:
            return []
        else:
            return ask.pricedim_set.all()

    def get_bid(self):
        """ Get the latest bid row associated with this player """
        bid = self.bid_set.last()
        return bid

    def get_bid_pricedims(self):
        bid = self.get_bid()
        if bid == None:
            return []
        else:
            return bid.pricedim_set.all()

    def get_pricedims(self):
        if self.roledesc == "Seller":
            return self.get_ask_pricedims()
        elif self.roledesc == "Buyer":
            return self.get_bid_pricedims()

    def set_buyer_data(self):
        """ This data is stored for analysis purposes. Payoffs set in group """
        rolenum_other = [ rn for rn in [1,2] if rn != self.contract_seller_rolenum][0]
        seller = self.group.get_player_by_role("S" + str(self.contract_seller_rolenum))
        seller_other = self.group.get_player_by_role("S" + str(rolenum_other))

        self.bid_total = seller.ask_total
        self.other_seller_ask_total = seller_other.ask_total
        self.mistake_size = max(0, self.bid_total - self.other_seller_ask_total)
        self.mistake_bool = 0 if self.mistake_size <= 0 else 1

        self.other_seller_ask_stddev = pstdev([ pd.value for pd in seller_other.get_ask().pricedim_set.all() ])


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
        if self.roledesc == "Seller":
            self.buyer_bool = False
            self.seller_bool = True
        else:
            self.buyer_bool = True
            self.seller_bool = False

    def role(self):
        return self.roledesc[0] + str(self.rolenum)


class Ask(Model):
    """ Stores details of a seller's ask """
    total = models.IntegerField(min=Constants.minprice, max=Constants.maxprice)
    stdev = models.FloatField(min=0)
    auto = models.BooleanField() # true if this ask was created automatically, else false
    manual = models.BooleanField() # true if this ask was created via maually changing a field, else false
    player = ForeignKey(Player)

    # def generate_pricedims(self):
    #     """ set through auto-generation of price dims """
    #     for i in range(self.player.subsession.dims):
    #
    #         # pd = PriceDim(ask=self, dimnum=i + 1)
    #         pd = self.pricedim_set.create(dimnum=i + 1)
    #         pd.save()

    def set_pricedims(self, pricedims):
        """ set through manual manipulation of fields """
        for i in range(self.player.subsession.dims):
            pd = self.pricedim_set.create(dimnum=i + 1, value=pricedims[i])
            pd.save()


class Bid(Model):
    """ Stores details of a buyer's bid. Not super useful at the moment given buyer's limited action space, but
        future-proofs the code somewhat. It also just gives a nice symmetry for how we deal with the two roles.
    """
    total = models.IntegerField(min=Constants.minprice, max=Constants.maxprice)
    player = ForeignKey(Player)

    def set_pricedims(self, pricedims):
        """ set through manual manipulation of fields """
        for i in range(self.player.subsession.dims):
            pd = self.pricedim_set.create(dimnum = i + 1, value=pricedims[i])
            pd.save()


class Contract(Model):
    """ Relates a bid and an ask in a successful exchange """
    ask = ForeignKey(Ask)
    bid = ForeignKey(Bid, blank=True, null=True)
    group = ForeignKey(Group)


class PriceDim(Model):   # our custom model inherits from Django's base class "Model"

    value = models.IntegerField()
    dimnum = models.IntegerField()

    # in reality, there will be either, but not both, an ask or a bid associated with each pricedim
    ask = ForeignKey(Ask, blank=True, null=True)    # creates 1:m relation -> this decision was made by a certain seller
    bid = ForeignKey(Bid, blank=True, null=True)
