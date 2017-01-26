from django.conf.urls import url
from otree.urls import urlpatterns

from . import views

# Seller AJAX
urlpatterns.append(url(r'^duopoly_rep_treat/autopricedims/$', views.AutoPricedims))
urlpatterns.append(url(r'^duopoly_rep_treat/manualpricedims/$', views.ManualPricedims))

# Wait game AJAX
urlpatterns.append(url(r'^duopoly_rep_treat/gamewaititercorrect/$', views.GameWaitIterCorrect))


# DATA
urlpatterns.append(url(r'^duopoly_rep_treat/data/$', views.ViewData))
urlpatterns.append(url(r'^duopoly_rep_treat/data/market/download$', views.MarketDataDownload, name="market_data_download"))
urlpatterns.append(url(r'^duopoly_rep_treat/data/market$', views.MarketDataView, name="market_data_view"))
urlpatterns.append(url(r'^duopoly_rep_treat/data/ask/download$', views.AskDataDownload, name="ask_data_download"))
urlpatterns.append(url(r'^duopoly_rep_treat/data/ask$', views.AskDataView, name="ask_data_view"))