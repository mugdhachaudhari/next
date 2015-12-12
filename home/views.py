from django.shortcuts import render
from login.views import *
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
from home.forms import *
from login.models import Users
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
import cx_Oracle
# Create your views here.

@login_required
def homepage(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	showcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('show', [m,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('home.html',{'row':row,'user': request.user})
	#n = notification.objects.filter(user=request.user, viewed=False)
	#return render_to_response(
	#'home.html',
	#{ 'user': request.user,#'notification':n 
	#}
	#)
	
@login_required
def home(request):
	u = User.objects.get(username = request.user)
	#m = request.session['userid']
	n = notification.objects.filter(user=request.user, viewed=False)
	request.session['userid'] = u.id 
	return render_to_response(
	'frame.html',{ 'user': request.user,'n':n})
	
@login_required
def ho(request):
    return render_to_response(
    'ho.html',
    { 'user': request.user }
    )

	
def allfeeds(request):
	return render_to_response(
    'allfeeds.html',
    { 'user': request.user }
    )

#def getid(request):
#	cursor=connection.cursor()
#	cursor.execute("select id from auth_user where username=request.user")
#	row=cursor.fetchone()
#	return HttpResponse(row)
	
def friends(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndscur = cursor.var(cx_Oracle.CURSOR).var
 #     cursor.callproc('showfriends', [21, 'frnds_cursor', err_cd, err_msg])
	result = cursor.callproc('showfriends', [m,frndscur, err_cd, err_msg])
	if result[2] == '0':
		row = result[1].fetchall()
	#	return HttpResponse(row)
		#variables = RequestContext(request, {'id': row})
		#return render_to_response('friends.html',variables,)
		#return render_to_response('friends.html',{'id':row})
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
		#return response
	return render_to_response('friends.html',{'id':row})

	
def neighbours(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	neighscur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showneighbours', [m,neighscur, err_cd, err_msg])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('neighbours.html',{'id':row})
	

def blocks(request):
	cursor = connection.cursor()
	m = request.session['userid']
	cursor.execute("select bid,blkdesc from blocks;")
	row = cursor.fetchall()
	return render_to_response('blocks.html',{'row':row})
		

def friendrequest(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	notifycur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showfrndreq', [m,notifycur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('friendrequest.html',{'row':row})
	
	
def notifications(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	notifycur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('notificationdisplay', [m,notifycur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('notifications.html',{'row':row})
	
	
def acceptfrndreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	acceptcur = cursor.var(cx_Oracle.CURSOR).var
	cursor.callproc('friendaccept', [m,x,'Y'])
	return render_to_response('template1.html')
	
	
	
def acceptblkreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	acceptcur = cursor.var(cx_Oracle.CURSOR).var
	cursor.callproc('friendaccept', [m,x,'Y'])
	return render_to_response('template1.html')
	
	
def sendblkreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	blkcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('blockrequest', [m,x, err_cd, err_msg])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('template3.html',{'row':row})
	
	
	
def declinefrndreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	acceptcur = cursor.var(cx_Oracle.CURSOR).var
	cursor.callproc('friendaccept', [m,x,'N'])
	return render_to_response('template2.html')

	
def messages(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		choice = request.POST['choice']
		if choice == 'f' or choice == 'n':
			return HttpResponseRedirect("/newmsg/")
		else:
			return HttpResponseRedirect("/newms/")
		
	else:
		form = MessageForm()
	variables = RequestContext(request, {
	'form': form,
	})
	return render_to_response(
	'msgsuccess.html',
	variables,
	)
	
def newmsg(request):
	if request.method == 'POST':
		form = NewmessageForm(request.POST)
		if form.is_valid:
			form.save()
			
			
		return HttpResponseRedirect('/message/')
	else:
		form = NewmessageForm()
	variables = RequestContext(request, {
	'form': form,
	})
 
	return render_to_response(
	'messages.html',
	variables,
	)
	
def message(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		choice = request.POST['choice']
		if choice == 'f' or choice == 'n':
			return HttpResponseRedirect("/newmsg/")
		else:
			return HttpResponseRedirect("/newms/")
		
	else:
		form = MessageForm()
	variables = RequestContext(request, {
	'form': form,
	})
	return render_to_response(
	'msgsuccess.html',
	variables,
	)
	
def newms(request):
	if request.method == 'POST':
		form = NewmessagesForm(request.POST)
		return HttpResponseRedirect('/messages.html/')
	else:
		form = NewmessagesForm()
	variables = RequestContext(request, {
	'form': form,
	})
 
	return render_to_response(
	'messages.html',
	variables,
	)
	
def frequest(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	cursor.callproc('updatefrnd', [m,x, err_cd, err_msg])
	variables = RequestContext(request, {'x':x})
	return render_to_response('template.html')
	#return HttpResponse(result[2])
	
	
def replymsg(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('replymsg', [x,m,frndthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('.html',{'row':row})
	
	
def reply(request):
	if request.method == 'POST':
		form = NewmessagesForm(request.POST)
		return HttpResponseRedirect('/messages.html/')
	else:
		form = NewmessagesForm()
	variables = RequestContext(request, {
	'form': form,
	})
 
	return render_to_response(
	'messages.html',
	variables,
	)
	
	
#def msgsuccess(request):
#	cursor = connection.cursor()
#	m = request.session['userid']
#	err_cd = cursor.var(cx_Oracle.NUMBER).var
#	err_msg = cursor.var(cx_Oracle.STRING).var
#	showcur = cursor.var(cx_Oracle.CURSOR).var
#	result = cursor.callproc('newmsg', [m,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
#	if result[2] == '0':
#		row = result[1].fetchall()
#	else:
#		response = HttpResponse()
#		response.write(result[2])
#		response.write(" ")
#		response.write(result[3])
#		row=''
#	return render_to_response('success.html',{'row':row})
	
	
def blockthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	blkthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('blockthreads', [m,blkthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('blockthreads.html',{'row':row})
	
	
def friendthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('friendthreads', [m,frndthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('friendthreads.html',{'row':row})
	
	
def next(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	blkthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('blockfeeds', [m,x,blkthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('next.html',{'row':row,'x':x})
	
def togo(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('friendfeeds', [m,x,frndthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('togo.html',{'row':row,'x':x})
	
	
def neighbourhoodthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourhoodthreads', [m,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('neighbourhoodthreads.html',{'row':row})
	
	
	
def neighbourthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourthreads', [m,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('neighbourthreads.html',{'row':row})
	
def allthreads(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	allthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allthreads', [m,allthreadcur, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('allthreads.html',{'row':row})
	
	
def to(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourfeeds', [m,x,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('to.html',{'row':row,'x':x})
	
	
def go(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	nbthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('neighbourhoodfeeds', [m,x,nbthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('go.html',{'row':row,'x':x})
	
	
def oo(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	allthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allfeeds', [m,x,allthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('oo.html',{'row':row,'x':x})

	
def show(request):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	showcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('show', [m,showcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[2] == '0':
		row = result[1].fetchall()
	else:
		response = HttpResponse()
		response.write(result[2])
		response.write(" ")
		response.write(result[3])
		row=''
	return render_to_response('home.html',{'row':row})
	
	
def newmessage(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		answer = form.cleaned_data['choices']
		variables = RequestContext(request, {'form': form})
		return render_to_response('next.html',variables)
