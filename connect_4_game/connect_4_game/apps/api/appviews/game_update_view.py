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
from api import serializers
from django.db.models import Prefetch
from utils import api_cache_key
from django.conf import settings
from utils import connect_4
from api.models import Game
from rest_framework.parsers import FileUploadParser
import uuid


class GameMoveView(APIView):

	def get_object(self, game_id):
		try:
			return Game.objects.get(id=game_id)
		except Game.DoesNotExist:
			raise serializers.game_update_serializer.MyCustomException(detail={"id":["game_id not found in the system"]},status_code=404)

	def check_uuid(self,id):
		try:
			uuid.UUID(id)
		except Exception:
			raise serializers.game_update_serializer.MyCustomException(detail={"id":["{} is not a valid uuid format and also not a valid game id . Please check your game id".format(id)]})

	def get(self, request, version, format=None, *args, **kwargs):

		

		game_id = self.request.query_params.get('id', None)


		self.check_uuid(game_id)
		request_id_obj = self.get_object(game_id)


		serializer = serializers.game_update_serializer.GameListingSerializer(request_id_obj,  context={'request': request})


		return Response({"detail": serializer.data}, status=status.HTTP_200_OK)

	def put(self,request, version, format=None):

		game_id = request.data.get('id', None)
		player_colour=request.data.get('player_colour', None)

		self.check_uuid(game_id)
		request_id_obj = self.get_object(game_id)
		print(request_id_obj)
		if request_id_obj.result!=0:
			return Response({"status":"success",'detail':{"Game ended":request_id_obj.get_result_display()},'code': 200}, status=200)
		game_serializer = serializers.game_update_serializer.GameSerializer(request_id_obj, data=request.data,  context={'request': request})

		if game_serializer.is_valid():

			game_serializer.save()

			game_object=Game.objects.get(id=game_id)
			if player_colour=='Red':
				if connect_4.check_winning(game_object.get_board,2):
					Game.objects.filter(id=game_id).invalidated_update(result=Game.RED_WINS)
					return Response({"status":"success",'detail':{"Game ended":Game.objects.get(id=game_id).get_result_display()},'code': 200}, status=200)
			else:
				if connect_4.check_winning(game_object.get_board,1):
					Game.objects.filter(id=game_id).invalidated_update(result=Game.YELLOW_WINS)
					return Response({"status":"success",'detail':{"Game ended":Game.objects.get(id=game_id).get_result_display()},'code': 200}, status=200)


			return Response({"status":"success",'detail':game_serializer.data,'code': 200}, status=200)
		else:
			return Response({"status":"error",'detail':game_serializer.errors,'code': 400}, status=400)





