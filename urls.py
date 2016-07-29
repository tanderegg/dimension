from django.conf.urls import url
from otree.default_urls import urlpatterns

from dimension.views import ClickView


urlpatterns.append(url(r'^click/$', ClickView.as_view(), name='click'))
