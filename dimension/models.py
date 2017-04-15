# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
import math
# </standard imports>


doc = """
TBD
"""

bibliography = (
    (
        'TBD'
    ),
)


class Constants(BaseConstants):
    name_in_url = 'dimension'
    players_per_group = 4
    num_practice_rounds = 2
    num_games = 3
    num_rounds = 6 + num_practice_rounds
    rounds_per_game = int((num_rounds-num_practice_rounds)/num_games)
    # This variable sets the number of prices used in each game in the exact 
    # order of this list
    prices_per_seller = [8,1,16]
    redeem_value = 800
    max_total_price = 800
    tokens_per_cent = 4
    starting_tokens = 500
    production_cost = 100
    # For convenience of testing the experience of players
    show_instructions = False


class Subsession(BaseSubsession):
    num_prices = models.PositiveIntegerField()
    sellers_per_group = models.PositiveIntegerField()
    buyers_per_group = models.PositiveIntegerField()
    game_number = models.PositiveIntegerField()
    real_round = models.BooleanField()

    def before_session_starts(self):
        self.assign_groups(self)
        self.set_game(self)
        self.assign_role_identifiers(self)

    @staticmethod
    def assign_groups(self): 
        # Randomly assign individuals to groups
        players = self.get_players()
        random.shuffle(players)
        group_matrix = []
        # chunk into groups of Constants.players_per_group
        ppg = Constants.players_per_group
        for i in range(0, len(players), ppg):
            group_matrix.append(players[i:i+ppg])
        self.set_groups(group_matrix)

        # Randomly Assign Roles within groups
        self.sellers_per_group = int(Constants.players_per_group/2)
        self.buyers_per_group = int(Constants.players_per_group - 
            self.sellers_per_group)

        for i, group in enumerate(self.get_groups()):
            group_roles = self.generate_roles()
            for player, role in zip(group.get_players(), group_roles):
                player.role_int = role
    
    @staticmethod
    def set_game(self):
        # Set which game number will be displayed to participants
        if self.round_number <= (Constants.num_practice_rounds+ 
            Constants.rounds_per_game):
            self.game_number = 1
        elif self.round_number <= (Constants.num_practice_rounds + 
            2*Constants.rounds_per_game):
            self.game_number = 2
        else:
            self.game_number = 3
        # Setting how many prices should be part of the decisions
        if self.game_number == 1:
            self.num_prices = Constants.prices_per_seller[0]
        elif self.game_number == 2:
            self.num_prices = Constants.prices_per_seller[1]
        else:
            self.num_prices = Constants.prices_per_seller[2]

    @staticmethod
    def assign_role_identifiers(self):
        for group in self.get_groups():
            group.set_identifier()

    def is_real_round(self):
        if self.round_number > Constants.num_practice_rounds:
            self.real_round = True
        else:
            self.real_round = False
        return self.real_round
   
    @staticmethod
    def generate_roles():
        sellers_per_group = int(Constants.players_per_group/2)
        buyers_per_group = int(Constants.players_per_group - sellers_per_group)
        num = int(Constants.players_per_group/2)
        roles = ['2'] * buyers_per_group + ['1'] * sellers_per_group
        roles = list(map(int, roles))
        random.shuffle(roles)
        return roles


class Group(BaseGroup):

    # This function takes in a numeric value and returns a list of all players 
    # within the group with the specified role integer
    def get_players_by_role(role_int):
        players = self.group.get_players()
        return [p for p in players if p.role_int == role_int]

    # Set an identifier so that individuals can follow a single seller from 
    # the seller select page to the round summary page
    def set_identifier(self):
        # Set identifier within each group for buyers
        buyers = [p for p in self.get_players() if p.role_int ==1]
        buyer_ids = list(range(1,self.subsession.buyers_per_group+1))
        random.shuffle(buyer_ids) 
        for i,buyer in enumerate(buyers):
            buyers[i].identifier = buyer_ids[i]
        # Set identifier within each group for sellers
        sellers = [p for p in self.get_players() if p.role_int ==2]
        seller_ids = list(range(1,self.subsession.sellers_per_group+1))
        random.shuffle(seller_ids)
        for i,seller in enumerate(sellers):
            sellers[i].identifier = seller_ids[i]

    # This will sum up the total cost of each product and keep this value stored
    # in the sellers row
    def total_cost(self):
        for player in self.get_players():
            if player.role_int == 1:
                if self.subsession.num_prices ==1:
                    player.seller_total_price = player.seller_price0
                elif self.subsession.num_prices == 8:
                    player.seller_total_price = sum([player.seller_price0,
                        player.seller_price1, player.seller_price2,
                        player.seller_price3, player.seller_price4,
                        player.seller_price5, player.seller_price6,
                        player.seller_price7])
                else:
                    player.seller_total_price = sum([player.seller_price0,
                    player.seller_price1, player.seller_price2, 
                    player.seller_price3, player.seller_price4,
                    player.seller_price5, player.seller_price6,
                    player.seller_price7, player.seller_price8, 
                    player.seller_price9, player.seller_price10,
                    player.seller_price11, player.seller_price12,
                    player.seller_price13, player.seller_price14,
                    player.seller_price15])
            
    # This will calculate the cost that each buyer must pay to the seller
    # selected for that round
    def buyer_cost(self):
        buyers = [p for p in self.get_players() if p.role_int == 2]
        for player_b in buyers:
            sellers = [p for p in self.get_players() if p.role_int == 1]
            for player_s in sellers:
                if player_s.identifier == (player_b.buyer_choice+1):
                    player_b.price_paid = player_s.seller_total_price

    # This calculates the number of sales that each buyer made in order to
    # calculate profits
    def number_sales(self):
        sellers = [p for p in self.get_players() if p.role_int==1]
        for seller in sellers:
            seller.sales = 0
            buyers = [p for p in self.get_players() if p.role_int==2]
            for buyer in buyers:        
                if buyer.buyer_choice == (seller.identifier-1):
                    seller.sales += 1
            seller.earnings = (seller.sales*
                (seller.seller_total_price-Constants.production_cost))
            
    def calculate_payoff(self):
        for player in self.get_players():
            if player.role_int == 2: 
                # Profits for buyers
                player.payoff = Constants.redeem_value - player.price_paid
            else: 
                # Profits for sellers
                player.payoff = player.earnings
            player.cum_payoff = sum([p.payoff for p in player.in_all_rounds()])

    def adjust_payoff(self):
        for player in self.get_players():
            if not self.subsession.is_real_round():
                player.payoff = 0

    def buyer_choice_to_seller_selected(self):
        buyers = [p for p in self.get_players() if p.role_int ==2]
        for buyer in buyers:
            buyer.seller_selected = buyer.buyer_choice + 1


class Player(BasePlayer):

    # Instruction Questions
    quiz_q1 = models.CharField(
        choices = ['0 tokens', '{} tokens'.format(Constants.redeem_value), 'It depends on the prices I set'],
        blank = True,
        widget = widgets.RadioSelect(),
        verbose_name = "How many tokens will you receive if you don't sell an object?")

    quiz_q2 = models.CharField(
        choices = ['0 tokens', '{} tokens'.format(Constants.redeem_value), 'It depends on the prices I set'],
        blank = True,
        widget = widgets.RadioSelect(),
        verbose_name = 'How many tokens will you receive if you sell an object?')

    # Role integer 1: seller, 2: buyer
    role_int = models.PositiveIntegerField(null = True, blank = True)

    # Storage of prices created by sellers
    seller_price0 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 1")
    seller_price1 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 2")
    seller_price2 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 3")
    seller_price3 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 4")
    seller_price4 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 5")
    seller_price5 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 6")
    seller_price6 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 7")
    seller_price7 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 8")
    seller_price8 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 9")
    seller_price9 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 10")
    seller_price10 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 11")
    seller_price11 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 12")
    seller_price12 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 13")
    seller_price13 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 14")
    seller_price14 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 15")
    seller_price15 = models.CurrencyField(min=0, null=True, blank=True,
        verbose_name = "Price 16")

    seller_total_price = models.CurrencyField(null=True, blank=True)
    # @TODO Make the prices a list which then has the appropriate length
    # for the subsession given the number of prices
    
    # How many sales does each seller make {0,...,n} where n is the number
    # of buyers
    sales = models.PositiveIntegerField(null = True, blank = True)
    # How many tokens does a seller earn in a single round
    earnings = models.PositiveIntegerField(null = True, blank = True)

    # Buyers choose a seller using the randomly assigned seller identifier
    buyer_choice = models.PositiveIntegerField(
        choices=[(i, 'Buy from seller %i' % (i+1)) for i in
                 range(0, int(Constants.players_per_group/2))] ,
        blank=True,
        widget=widgets.RadioSelect(),
        verbose_name='And you will')  
    seller_selected = models.PositiveIntegerField(blank = True)
    # This will be the sum of prices of the seller a buyer selects
    price_paid = models.PositiveIntegerField(null = True, blank = True)

    # Both the buyers and sellers will need a randomly assigned identifier in
    # order to reference each anonymized player type
    identifier = models.PositiveIntegerField(null = True, blank = True)

    # Cumulative profits
    cum_payoff = models.PositiveIntegerField(null = True, blank = True)

    # Number of clicks on the buyer wait page.
    clicks = models.PositiveIntegerField(default=0)
    
    def role(self):
        return {1:'seller', 2:'buyer'}[self.role_int]

    def add_click(self):
        self.clicks = self.clicks + 1
        self.save()
        return self.clicks
