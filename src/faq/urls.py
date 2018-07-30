from django.urls import path

from .views import eos_911, news, repos, steem, testnets, twitter, youtube

urlpatterns = [
    path('eos-911/', eos_911, name='eos-911'),
    path('news/', news, name='news'),
    path('repos/', repos, name='repos'),
    path('steem/', steem, name='steem'),
    path('testnets/', testnets, name='testnets'),
    path('twitter/', twitter, name='twitter'),
    path('youtube/', youtube, name='youtube'),
]