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
from django.db import connection



# Create your views here.

 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # registration = Registration.objects.create_registration(
            # #username=form.cleaned_data['username'],
            # password=form.cleaned_data['password1'],
            # email=form.cleaned_data['email']
			#)
            registration = Registration(userid = default, email = form.cleaned_data['email'], password=form.cleaned_data['password1'])
            registration.save()
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )


# def nextvalue():
	
	# return 
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response(
    'home.html',
    { 'registration': request.registration }
    )



# def login(request):
	# # if request.method != 'POST':
		# # raise Http404('Only POSTs are allowed')
	# try:
		# u = Registration.objects.get(email=request.POST['email'], enddate = date(9999,12,31))
		# if u.password == request.POST['password']:
			# request.session['user_id'] = u.userid
			# return HttpResponseRedirect('/you-are-logged-in/')
	# except Registration.DoesNotExist:
		# return HttpResponse("Your username and password didn't match.")
		
# def logout(request):
    # try:
        # del request.session['user_id']
    # except KeyError:
        # pass
    # return HttpResponse("You're logged out.")
