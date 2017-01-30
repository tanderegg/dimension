from .models import Constants, Subsession, Player, Group
from survey.models import Subsession as SubsessionSurvey
from survey.models import Player as PlayerSurvey
from otree.models.session import Session
from . import models
from otree.export import get_field_names_for_csv
from django.http import HttpResponse
import datetime
import csv


# HELPER METHODS
def export_csv(title, headers, body):
    # filename = get_filename("marketdata")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{} (accessed {}).csv"'.format(title,
        datetime.date.today().isoformat()
    )

    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(body)

    return response

def list_from_obj(fieldnames, obj):
    """
        Small helper function to create a list from an object <obj> using <fieldnames>
        as attributes.
    """
    data = []
    for f in fieldnames:
        if type(obj) == dict:
            data.append(obj[f])
        else:
            data.append("" if getattr(obj, f)==None else getattr(obj, f))

    return data


def get_headers_simple():
    session_fns = ['code', 'id']
    session_fns_display = ['session_' + fn for fn in session_fns]
    group_fns = ['id_in_subsession']
    group_fns_display = ['group_id']
    participant_fns = ['code', 'id_in_session']
    participant_fns_display = ['participant_' + fn for fn in participant_fns]

    return session_fns, session_fns_display, group_fns, group_fns_display, participant_fns, participant_fns_display


def get_pd_list(pricedims, dims, maxdim):
    """ return list of pricedims with appropriate number of blank cells """
    if len(pricedims) == 0:
        # only here if this row is not yet populated (checking data mid-stream)
        pricedim_list = [""] * maxdim
    else:
        pricedim_list = []
        for i in range(1, maxdim + 1):
            if i <= dims:
                pricedim_list += [pricedims[i - 1].value]
            else:
                pricedim_list += [""]

    return pricedim_list


# EXPORT FUNCTIONS
def export_asks():
    """
        Sends headers and data to views for csv data viewing/export.
        Much code taken from:
            https://github.com/WZBSocialScienceCenter/otree_custom_models/blob/master/example_decisions/views.py
    """
    maxdim = max(Constants.treatmentdims)
    body = []
    session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

    # Create the header list
    subsession_fns = ['round_number', 'practiceround', 'treatment']
    player_fns = ['id_in_group', 'rolenum']
    ask_fns = ['total', 'stdev', 'auto', 'manual']

    headers = session_fns_d + subsession_fns + group_fns_d + participant_fns_d + player_fns + ask_fns
    for i in range(1, maxdim + 1):
        headers.append("p" + str(i))

    # get all sessions, order them by label
    sessions = Session.objects.order_by("code")
    # loop through all sessions
    for session in sessions:
        session_list = list_from_obj(session_fns, session)

        # loop through all subsessions (i.e. rounds) ordered by round number
        subsessions = sorted(models.Subsession.objects.filter(session=session, treatment__gt=1),
                             key=lambda x: x.round_number)
        for subsession in subsessions:
            subsession_list = list_from_obj(subsession_fns, subsession)

            # loop through all groups ordered by ID
            groups = sorted(subsession.get_groups(), key=lambda x: x.id_in_subsession)
            for group in groups:
                group_list = list_from_obj(group_fns, group)

                # loop through all players ordered by ID
                players = sorted(models.Player.objects.filter(group=group, roledesc="Seller"),
                                 key=lambda x: x.participant.id_in_session)
                for player in players:
                    participant = player.participant
                    player_list = list_from_obj(participant_fns, participant) + list_from_obj(player_fns, player)

                    asks=sorted(models.Ask.objects.filter(player=player), key=lambda x: x.id)
                    for ask in asks:
                        ask_list = list_from_obj(ask_fns, ask)

                        pds = sorted(ask.pricedim_set.all(), key=lambda x: x.dimnum)
                        pd_list = get_pd_list(pds, subsession.dims, maxdim)

                        body.append( session_list + subsession_list + group_list + player_list + ask_list + pd_list )

    return headers, body


def export_contracts():

    maxdim = max(Constants.treatmentdims)
    body = []
    session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

    player_fns = []
    subsession_fns = ["round_number", "realround", "treatment"]
    player_fns_d = ["seller_code", "seller_group_id", "buyer_code", "buyer_group_id"]
    contract_fns = ['total', 'stdev']
    pricedim_fns = ["p" + str(i) for i in range(1, maxdim + 1)]

    sessions = Session.objects.order_by("code")
    for session in sessions:
        session_list = list_from_obj(session_fns, session)

        # I believe this method excludes subsessions from other apps, and thus we do not need to filter on app name
        subsessions = Subsession.objects.filter(session=session)
        for subsession in subsessions:
            subsession_list = list_from_obj(subsession_fns, subsession)

            groups = subsession.get_groups()
            for group in groups:
                group_list = list_from_obj(group_fns, group)

                contracts = group.contract_set.all()
                for contract in contracts:
                    seller = contract.ask.player
                    buyer = contract.bid.player

                    player_list = [seller.participant.code, seller.id_in_group, buyer.participant.code,
                                   buyer.id_in_group]

                    contract_list = [contract.ask.total, contract.ask.stdev]

                    pd_list = get_pd_list(seller.get_pricedims(), subsession.dims, maxdim)

                    body.append(session_list + subsession_list + group_list + player_list + contract_list + pd_list)

    headers = session_fns_d + subsession_fns + group_fns_d + player_fns_d + contract_fns + pricedim_fns

    return headers, body


def export_surveydata():
    """

        :return:
    """
    body=[]

    subsession_fns = []
    player_fns = []
    session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

    sessions = Session.objects.order_by("code")
    for session in sessions:
        session_list = list_from_obj(session_fns, session)

        subsessions = [ss for ss in session.get_subsessions() if ss.__class__._meta.app_config.name=="survey"]
        for subsession in subsessions:
            # print(subsession._meta.app_config.name)
            subsession_fns = subsession_fns or get_field_names_for_csv(subsession.__class__)
            subsession_list = list_from_obj(subsession_fns, subsession)

            players = sorted(subsession.get_players(), key=lambda x: x.participant.id_in_session)
            for player in players:
                player_fns = player_fns or get_field_names_for_csv(player.__class__)
                participant = player.participant

                player_list = list_from_obj(participant_fns, participant) + list_from_obj(player_fns, player)

                body.append(session_list + subsession_list + player_list)

    headers = session_fns_d + subsession_fns + participant_fns_d + player_fns

    return headers, body

def get_market_headers(maxdim):
    """ Helper function to create headers """
    hdrs = []

    for role in ("S1", "S2"):
        for suffix in ["participant_id_in_session", "participant_code", "payoff", "ask_total", "ask_stdev", "numsold"]:
            hdrs.append(role + "_" + suffix)
        for i in range(1, maxdim + 1):
            hdrs.append(role + "_p" + str(i))

    for role in ("B1", "B2"):
        for suffix in ["participant_id_in_session", "participant_code", "payoff", "bid_total","contract_seller_rolenum"]:
            hdrs.append(role + "_" + suffix)

    return hdrs

def get_market_row(group, dims, maxdim):
    """ Helper function to cteate market-level data """
    market_list = []
    for role in ("S1", "S2"):
        seller = group.get_player_by_role(role)
        market_list += [seller.participant.id_in_session, seller.participant.code, seller.payoff,
                        seller.ask_total, seller.ask_stdev, seller.numsold]

        # add price dims and appropriate number of blank spaces
        market_list += get_pd_list(seller.get_pricedims(), dims, maxdim)

    for role in ("B1", "B2"):
        buyer = group.get_player_by_role(role)
        market_list += [buyer.participant.id_in_session, seller.participant.code,
                        buyer.payoff, buyer.bid_total, buyer.contract_seller_rolenum]

    return market_list

def export_marketdata():
    """

        :return:
    """

    maxdim = max(Constants.treatmentdims)
    body = []
    session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

    subsession_fns = ["round_number", "realround", "treatment"]
    group_fns = get_field_names_for_csv(Group)
    market_fns = get_market_headers(maxdim)

    headers = session_fns_d + subsession_fns + group_fns + market_fns

    sessions = Session.objects.order_by("code")
    for session in sessions:
        session_list = list_from_obj(session_fns, session)

        # I believe this method excludes subsessions from other apps, and thus we do not need to filter on app name
        subsessions = Subsession.objects.filter(session=session)
        for subsession in subsessions:
            subsession_list = list_from_obj(subsession_fns, subsession)

            groups = subsession.get_groups()
            for group in groups:

                group_list = list_from_obj(group_fns, group)
                market_list = get_market_row(group, subsession.dims, maxdim)

                # players = sorted(group.get_players(), key=lambda x: x.participant.id_in_session)
                # for player in players:
                #     player_fns = player_fns or get_field_names_for_csv(player.__class__)

                body.append(session_list + subsession_list + group_list + market_list)

    return headers, body


def export_combineddata():
    """
        Getting ALL the fields in one place
        This will not return all Asks (only latest)
        This will not return response times
        This will not return payment data
        :return: csv headers and body for output
    """
    maxdim = max(Constants.treatmentdims)
    body = []
    # only using the participant headers from this ...
    session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

    session_fns = ["id"] + get_field_names_for_csv(Session)
    metadata_fns = ["treatmentorder", "date", "time"]
    subsession_fns = get_field_names_for_csv(Subsession) # this will only get the market subsessions (not survey)
    group_fns = get_field_names_for_csv(Group)
    market_fns = get_market_headers(maxdim)
    player_fns = get_field_names_for_csv(Player)
    pricedim_fns = ["p" + str(i) for i in range(1, maxdim + 1)]
    survey_fns = get_field_names_for_csv(PlayerSurvey)

    headers = session_fns + metadata_fns + subsession_fns + group_fns + market_fns + participant_fns_d + player_fns + \
              pricedim_fns + survey_fns

    sessions = Session.objects.order_by("pk")
    for session in sessions:
        session_list = list_from_obj(session_fns, session)
        metadata_list = list_from_obj(metadata_fns, session.config)

        # I believe this method excludes subsessions from other apps, and thus we do not need to filter on app name
        subsessions = Subsession.objects.filter(session=session)
        for subsession in subsessions:
            subsession_list = list_from_obj(subsession_fns, subsession)

            groups = subsession.get_groups()
            for group in groups:
                group_list = list_from_obj(group_fns, group)
                market_list = get_market_row(group, subsession.dims, maxdim)

                players = group.get_players()
                for player in players:
                    participant = player.participant
                    participant_list = list_from_obj(participant_fns, participant)
                    player_list = list_from_obj(player_fns, player)
                    # TODO price dims
                    pricedim_list = get_pd_list(player.get_pricedims(), subsession.dims, maxdim)

                    # subsession_survey = SubsessionSurvey.objects.get(session=session)
                    # players_survey = subsession_survey.get_players()

                    player_survey = PlayerSurvey.objects.get(session=session, participant__code=participant.code)
                    survey_list = list_from_obj(survey_fns, player_survey)


                    body.append(session_list + metadata_list + subsession_list + group_list + market_list +
                                participant_list + player_list + pricedim_list + survey_list)

    return headers, body