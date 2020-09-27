# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple
from django.shortcuts import render
from itertools import groupby
from operator import itemgetter

import datetime, json
import math

from datetime import timedelta
from datetime import tzinfo
from dateutil import parser
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.core.urlresolvers import resolve
from django.db.models import Count
from django.db.models import F
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.db.models import Sum
from django.dispatch import receiver
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
