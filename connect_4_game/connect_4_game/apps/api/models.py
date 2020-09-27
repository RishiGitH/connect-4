# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import URLValidator
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache
from django.db.models import F, Q, Min, Max, Sum, Count
from django.core.validators import MaxValueValidator, MinValueValidator
import hashlib
import datetime
import os, uuid, requests, csv, io,json
from functools import partial
from contextlib import closing
from django.core.exceptions import ValidationError
import urllib.request
from utils.config import conf



def get_staring_board():
	return json.dumps([[0 for _ in range(conf.column_count)] for _ in range(conf.row_count)])


class Game(models.Model):
	IN_PROGRESS=0
	RED_WINS = 1
	YELLOW_WINS = 2

	RESULT_CHOICES = (
		(RED_WINS, 'Red Wins the Game'),
		(YELLOW_WINS, 'Yellow Wins the Game'),
		(IN_PROGRESS,'Game is in Progress'),
	)

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	board = models.TextField(default=get_staring_board)
	move_count=models.IntegerField(default=0)
	result= models.PositiveSmallIntegerField(choices=RESULT_CHOICES, default=IN_PROGRESS)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)


	@property
	def get_board(self):
		return json.loads(self.board)
	



	@property
	def get_moves(self):

		return Move.objects.filter(game=self)

	class Meta:
		db_table = 'game_records'

	def __str__(self):
		return '(id:%s)' % (self.id)



class Move(models.Model):


	COLOUR_CHOICES = (
		('Red', 'Red'),
		('Yellow', 'Yellow'),
	)

	id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	game= models.ForeignKey(Game)
	player_colour=models.CharField(max_length=20,choices=COLOUR_CHOICES)
	column=models.IntegerField(
        validators=[
            MaxValueValidator(conf.column_count-1),
            MinValueValidator(0)
        ]
     )
	move_number=models.IntegerField()
	added_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'game_moves'

	def __str__(self):
		return '(id:%s)' % (self.id)


