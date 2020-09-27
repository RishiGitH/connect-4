# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
import datetime


def common(request):
	return {
		'debug': settings.DEBUG,
		'MEDIA_URL': settings.MEDIA_URL,
	}