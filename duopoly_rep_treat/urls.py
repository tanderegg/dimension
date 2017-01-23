from django.conf.urls import url
from otree.urls import urlpatterns

from . import views

urlpatterns.append(url(r'^duopoly_rep_treat/autopricedims/$', views.AutoPricedims))