# Don't change anything in this file.
from .. import models
import otree.views
import otree.test
from otree.common import Currency as c, currency_range

class Page(otree.views.Page):
    is_debug = False
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()
        self.player = models.Player()


class WaitPage(otree.views.WaitPage):
    is_debug = False
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()


class Bot(otree.test.Bot):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()
        self.player = models.Player()


