"""bayes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from core import views
from rest_framework import routers
from api.views import BaysianNetViewSet, LogSessionViewSet, GameSessionViewSet

router = routers.DefaultRouter()
router.register(r'nets', BaysianNetViewSet)
router.register(r'logs', LogSessionViewSet)
router.register(r'session', GameSessionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^baysianet/new/$', views.baysianet_new, name='baysianet_new'),
    url(r'^baysianet/(?P<pk>[0-9]+)/$', views.baysianet_detail, name='net_detail'),
    url(r'^competence/new/(?P<baysianet_pk>[0-9]+)$', views.competence_new, name='competency_new'),
    url(r'^baysianet/hierarchy/new/(?P<baysianet_pk>[0-9]+)$', views.hierarchy_new, name='hierarchy_new'),
    url(r'^competence/variable/new/(?P<competency_pk>[0-9]+)$', views.variable_new, name='variable_new'),
    url(r'^competence/(?P<pk>[0-9]+)/$', views.competence_detail),
    url(r'^api/', include(router.urls)),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^register/$', views.register),
    url(r'^games/$', views.games, name='games'),
    url(r'^games/play/(?P<game_pk>[0-9]+)$', views.play, name='play'),
    url(r'^relatorios/(?P<game_pk>[0-9]+)$', views.relatorios, name='relatorios'),
    url(r'^relatorios/(?P<user_pk>[0-9]+)/(?P<game_pk>[0-9]+)$', views.relatorio_individual, name='relatorio_individual'),
    url(r'^relatorios/simulator/(?P<session_pk>[0-9]+)$', views.simulator, name='simulator'),

]
