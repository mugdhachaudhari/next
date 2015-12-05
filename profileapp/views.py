# Create your views here.
from profileapp.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
# from login.models import Registration
# from login.models import Users
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle



# Create your views here.


def profile(request):
	u = User.objects.get(username = request.user)
	if request.method == 'POST':
		usern_form = UserForm(request.POST, request.FILES , prefix = "usern", initial = {'username' : request.user, 'email' : u.email})
		up_form = ProfileForm(request.POST, request.FILES, prefix = "up", instance=request.user.profile)
# 		form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
# 		return HttpResponse(request.FILES.get('photopath', False).name)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/home/')
		if usern_form.is_valid() and up_form.is_valid():
			if usern_form.has_changed():
				usern_form.save()
			up_form.save()
			return HttpResponseRedirect('/home/')
	else:
		user = request.user
		profile = user.profile
# 		form = ProfileForm(iuest.unitial={'username' : reqser})
		usern_form = UserForm(prefix = "usern", initial = {'username' : request.user, 'email' : u.email})
		up_form = ProfileForm(prefix = "up", instance = profile)	
# 		form = ProfileForm(instance = profile)
	variables = RequestContext(request, {'username': request.user, 'up_form': up_form, 'usern_form': usern_form})
	return render_to_response('profile.html',variables,)

