# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.pagination import PageNumberPagination
from utils import api_cache_key
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import authentication
from rest_framework_extensions.cache.decorators import (cache_response)
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import status
from api import serializers
from api.models import Game




class GameStartView(APIView,LimitOffsetPagination):



	def get(self, request, version, format=None, *args, **kwargs):

		game_obj=Game.objects.create()
		return Response({"status":"success","detail": {'id':game_obj.id},'code': 200}, status=200)

