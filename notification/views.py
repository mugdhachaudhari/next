from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from login.models import notification
from login.models import Users
# Create your views here.

def show_notification(request, notification_id):
	n = notification.objects.get(id=notification_id)
	return render_to_response('notification.html',{'notification':n})

def delete_notification(request,notification_id):
	n= notification.objects.get(id=notification_id)
	n.viewed = True
	n.save()
	
	return HttpResponseRedirect('/home/')