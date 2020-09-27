
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework.routers import SimpleRouter, DefaultRouter
import os
from api import appviews
from api.appviews import game_update_view
from api.appviews import game_start_view
import os


router_v1 = SimpleRouter()

urlpatterns = [

	# url(r'^api/(?P<version>[1])/submit_job', submit_job_views.FileUploadView.as_view(), name='api.submit_job_view'),

	url(r'^api/(?P<version>[1])/game/start', game_start_view.GameStartView.as_view(), name='api.game_start_view'),
	url(r'^api/(?P<version>[1])/game', game_update_view.GameMoveView.as_view(), name='api.game_move_view'),

]
