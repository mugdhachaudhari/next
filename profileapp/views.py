# Create your views here.
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from login.models import Registration
from login.models import Users
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle



# Create your views here.

 
def profile(request):
	return HttpResponse("Update your profile")	
