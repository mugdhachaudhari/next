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
from home.forms import *
# from home.models import Users
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
import cx_Oracle
from nextnbr.settings import MEDIA_URL
# Create your views here.

@login_required
def homepage(request):
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
	# n = notification.objects.filter(user=request.user, viewed=False)
	request.session['userid'] = u.id
	prfl = request.user.profile
	if not prfl.firstname:
		return HttpResponseRedirect('/accounts/profile/', {'alert' : True})
	return render_to_response(
	'frame.html',{ 'user': request.user})
	
@login_required
def ho(request):
	prfl = request.user.profile
	return render_to_response('ho.html',{ 'user': request.user, 'MEDIA_URL' : MEDIA_URL, 'prfl' : prfl })

@login_required	
def allfeeds(request):
	return render_to_response(
    'allfeeds.html',
    { 'user': request.user }
    )

	
	
@login_required	
def msg(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(x)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('allfeeds', [m,x,frndthreadcur, err_cd, err_msg])
	#return HttpResponse(result[2])
	if result[3] == '0':
		row = result[2].fetchall()
	else:
		response = HttpResponse()
		response.write(result[3])
		response.write(" ")
		response.write(result[4])
		row=''
	return render_to_response('msg.html',{'row':row,'x':x})
#def getid(request):
#	cursor=connection.cursor()
#	cursor.execute("select id from auth_user where username=request.user")
#	row=cursor.fetchone()
#	return HttpResponse(row)
@login_required
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

@login_required	
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
	
@login_required
def blocks(request):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	notifycur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('showblocks', [m, err_cd, err_msg])
	#return HttpResponse(result[1])
	if result[1] == '0':
		lat = request.user.profile.loc.latitude
		lng = request.user.profile.loc.longitude
		listblks = []
		blks = Blocks.objects.all()
		for x in blks:
			ymax = Decimal(x.nec.split(',')[0])
			xmax = Decimal(x.nec.split(',')[1])
			ymin = Decimal(x.swc.split(',')[0])
			xmin = Decimal(x.swc.split(',')[1])
#         	rx = range(xmax, xmin)
#         	ry = range(ymax, ymin)
			if lng >= xmax and lng <= xmin and lat >= ymax and lat <= ymin :
				listblks.append(x)
#     ne =nec.split(',')[0] request.user.profile.loc.latitude
#     sw = request.user.profile.loc.longitude
#     bbox = ("XMIN = " ,xmin," YMIN = ", ymin, " XMAX  = ", xmax, " YMAX ",  ymax)
#     geom = Polygon.from_bbox(bbox)
#     return HttpResponse(bbox)
	return HttpResponse(listblks)
	#else if result[1] == 1:
	#return render_to_response('blocks.html',{'row':row})
		
@login_required
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
	
@login_required	
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
	
@login_required
def acceptfrndreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	acceptcur = cursor.var(cx_Oracle.CURSOR).var
	cursor.callproc('friendaccept', [m,x,'Y'])
	return render_to_response('template1.html')
	
	
@login_required	
def acceptblkreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	acceptcur = cursor.var(cx_Oracle.CURSOR).var
	cursor.callproc('friendaccept', [m,x,'Y'])
	return render_to_response('template1.html')
	
@login_required
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
	
	
@login_required	
def declinefrndreq(request,x):
	cursor = connection.cursor()
	m = request.session['userid']
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	acceptcur = cursor.var(cx_Oracle.CURSOR).var
	cursor.callproc('friendaccept', [m,x,'N'])
	return render_to_response('template2.html')
	

@login_required	
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

@login_required	
def newmsg(request):
	if request.method == 'POST':
		form = NewmessageForm(request.POST)
		cursor = connection.cursor()
		m = request.session['userid']
	#return HttpResponse(m)
		err_cd = cursor.var(cx_Oracle.NUMBER).var
		err_msg = cursor.var(cx_Oracle.STRING).var
		frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
		result = cursor.callproc('newmsg', [m,title,textbody,frndthreadcur, err_cd, err_msg])
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
		#return HttpResponseRedirect('/newmesg/')
	#else:
	#	form = NewmessageForm()
	#variables = RequestContext(request, {
	#'form': form,
	#})
 
	#return render_to_response(
	#'messages.html',
	#variables,
	#)
	
@login_required	
def message(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		choice = request.POST['choice']
		if choice == 'F' or choice == 'N':
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
	
@login_required	
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
	
@login_required
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
	
@login_required	
def newmesg(request):	
	cursor = connection.cursor()
	m = request.session['userid']
	#return HttpResponse(m)
	err_cd = cursor.var(cx_Oracle.NUMBER).var
	err_msg = cursor.var(cx_Oracle.STRING).var
	frndthreadcur = cursor.var(cx_Oracle.CURSOR).var
	result = cursor.callproc('newmsg', [x,m,frndthreadcur, err_cd, err_msg])
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
	
@login_required	
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
	
@login_required	
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
	
@login_required
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
	
@login_required	
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
	
@login_required	
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

@login_required	
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
	
@login_required	
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
	
	
@login_required	
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

@login_required	
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
	
@login_required	
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
	
@login_required	
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
	
@login_required	
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

@login_required
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
	
@login_required
def newmessage(request):
	if request.method == 'POST':
		form = MessageForm(request.POST)
		answer = form.cleaned_data['choices']
		variables = RequestContext(request, {'form': form})
		return render_to_response('next.html',variables)
