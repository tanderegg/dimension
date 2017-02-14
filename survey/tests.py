# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    # def play_round(self):

    #     self.submit(views.Demographics, {
    #         'q_country': 'BS',
    #         'q_age': 24,
    #         'q_gender': 'Male'})

    #     self.submit(views.RiskQuestions, {
    #         'q_risk1': 1,
    #         'q_risk2': 1,
    #         'q_risk3': 1
    #     })

    # def validate_play(self):
    #     pass

    def play_round(self):
        risk1_answer = 1
        yield(views.Risk1, {"q_risk1" : risk1_answer})
        if (risk1_answer == 1):
            yield(views.Risk2, {"q_risk2" : 'A 100% chance of $17.50'})
        if (risk1_answer == 2):
            yield(views.Risk3, {"q_risk3" : 'A 50% chance of $35'})
        yield(views.Risk4, {"q_risk4" : '2'})
        yield(views.NFC1, {"q_nfc1" : 1, "q_nfc2" : 1, "q_nfc3" : 1})
        yield(views.NFC2, {"q_nfc4" : 1, "q_nfc5" : 1, "q_nfc6" : 1})
        yield(views.NFC3, {"q_nfc7" : 1, "q_nfc8" : 1})
        yield(views.SubjNumeracy1, {'q_subjNum1' : '2', 'q_subjNum2' : '2', 'q_subjNum3' : '2'})
        yield(views.SubjNumeracy2, {'q_subjNum4' : '2', 'q_subjNum5' : '2', 'q_subjNum6' : '2'})
        yield(views.SubjNumeracy3, {'q_subjNum7' : '2', 'q_subjNum8' : '2'})
        yield(views.ObjNumeracy, {'q_objNum1' : 1, 'q_objNum2' : 1, 'q_objNum3' : 1})
        yield(views.Demographics1, {'q_experience' : '0', 'q_gender' : "Male", 'q_english' : "Yes", 'q_age' : 21})
        yield(views.Demographics2, {'q_course_micro' : True, 'q_course_mkt' : True, 'q_course_law' : True})
        yield(views.FutureStudies, {"q_futureStudies" : 'Yes, I would like to be contacted for future studies'})
        #yield(views.Splash)




