from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_page
import operator

try:
	import json
except ImportError:
	import simplejson as json
from django.template.context import RequestContext
from django.template.loader import get_template

def index(request):
    return render(request, 'login.html')