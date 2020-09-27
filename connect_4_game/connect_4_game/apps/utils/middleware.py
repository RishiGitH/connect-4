# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sessions.models import Session
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.conf import settings
from importlib import import_module
from django.core.cache import cache
from django.middleware.csrf import get_token
from django.template.response import ContentNotRenderedError
import urllib
import ast, random
from django.middleware.common import BrokenLinkEmailsMiddleware
from django.db.models import F, Q
from django.utils.encoding import force_text
import traceback
import sys
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from random import shuffle
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login


engine = import_module(settings.SESSION_ENGINE)

from django.template import Template, Context


from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
import inspect


class CachedTemplateMiddleware(MiddlewareMixin):

	def custom_url(self, name, **kwargs):
		return reverse(name, kwargs=kwargs)

	def process_view(self, request, view_func, view_args, view_kwargs):
		#webp support check and set for request object
		cached_views = settings.CACHED_VIEWS.keys()

		ctx = {
			'request': request,
			'csrf_token': get_token(request),
			'static': staticfiles_storage.url,
			'url':self.custom_url,
			'MEDIA_URL': settings.MEDIA_URL,
		}

		cache_key = '.'.join(['apicaching',request.method.lower(), str(request.path)])

		if request.method == 'GET':
			response = None
			if 'magicflag' in request.GET:
				request_get_items = dict(request.GET)
				request_get_items.pop('magicflag', None)
				cache_key += '?' + urllib.parse.urlencode(request_get_items).encode('ascii', 'ignore').decode('ascii')
				cache_key = '*' + cache_key
				try:
					cache.delete(cache.keys(cache_key)[0]) #cache.get(cache_key, None)
				except:
					pass;
		else:
			response = view_func(request, *view_args, **view_kwargs)

		view_ctx = self._get_ctx_for_view(request, view_func, view_kwargs)
		ctx.update(view_ctx)

		if response and 'text' in response.get('content-type'):
			try:
				t = Template(response.content.decode('utf-8'))
				# response.content = t.render(ctx)
				response.content = t.render(Context(ctx))
			except Exception: # for django templates
				pass

		return response

	def _get_ctx_for_view(self, request, view_func, view_kwargs):
		ctx = {}
		return ctx


