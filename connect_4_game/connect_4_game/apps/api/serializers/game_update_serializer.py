# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
import ast
import urllib, re
from collections import OrderedDict
from copy import deepcopy
from rest_framework.settings import api_settings
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from django.db.models import Q, Max, Min
from django.conf import settings

from django.contrib.auth.models import User
from utils.config import conf
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from datetime import datetime
import json
from django.db.models import Count
from collections import defaultdict
import random
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from api.models import Game,Move
from utils import connect_4

class MyCustomException(PermissionDenied):
	status_code = status.HTTP_400_BAD_REQUEST
	default_detail = "Custom Exception Message"
	default_code = 'invalid'

	def __init__(self, detail, status_code=None):
		if status_code is not None:
			self.status_code = status_code
		self.detail = {"status": "error","detail": detail,"code": self.status_code}









class GameMoveSerializer(serializers.ModelSerializer):

	class Meta:
		model = Move
		fields = (
			'id','player_colour','column','move_number','added_on'
		)



class GameListingSerializer(serializers.ModelSerializer):


	moves=GameMoveSerializer( source='get_moves',
        many=True
    )


	class Meta:
		model = Game
		fields = (
			'id','moves'

		)






class MoveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Move
		fields = (
			'player_colour','column'
		)


					

class GameSerializer(serializers.ModelSerializer):
	
	move=MoveSerializer(write_only=True)
	class Meta:
		model = Game
		fields = (
			'id','board','move','move_count','updated_on'

		)
		read_only_fields = ('board','move_count','updated_on')

		



	def update(self,instance,validated_data):

		print(validated_data)
		move_data=validated_data.get('move')
		column=move_data.get('column')
		player_colour=move_data.get('player_colour')
		print(player_colour)
		game_object=instance

		move_count=game_object.move_count+1

		if move_count%2==0:

			if player_colour=='Red':
				player_coin=2
			else:
				raise MyCustomException(detail={"player_colour":["Invalid player_colour.Right Now its Red Turn "]})

		else:

			if player_colour=='Yellow':
				player_coin=1
			else:
				raise MyCustomException(detail={"player_colour":["Invalid player_colour.Right Now its Yellow Turn "]})


		game_board=game_object.get_board

		row=connect_4.get_row(game_board,column)

		if row==None:
			raise MyCustomException(detail={"column":["Invalid column move .Column already filled"]})

		game_board[row][column]=player_coin

		Game.objects.filter(id=instance.id).invalidated_update(board=json.dumps(game_board),move_count=move_count)

		Move.objects.create(game=game_object,player_colour=player_colour,column=column,move_number=move_count)

		return Game.objects.get(id=instance.id)



