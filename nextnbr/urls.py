"""nextnbr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from login.views import *
#from django.contrib import user_messages
from profileapp.views import *
from home.views import *
from mail.views import *
from notification.views import *
#from django_messages.urls import *
#from myapp.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^show/(?P<notification_id>\d+)/$',show_notification),
	url(r'^delete/(?P<notification_id>\d+)/$',delete_notification),
	url(r'^homepage/', 'profileapp.views.homepage'),
    url(r'^$', 'django.contrib.auth.views.login'),
	url(r'^friendrequest/$', friendrequest),
    url(r'^logout/$', logout_page),
	#url(r'^acceptfrndreq/$', acceptfrndreq),
	url(r'^send_email/$', send_email),
	# url(r'^accounts/login/$', login_page),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
	url(r'^home/homepage/$', homepage),
	#url(r'^messages/',django_messages.urls)
	url(r'^home/ho/allfeeds/$', allfeeds),
	url(r'^home/ho/$', ho),
	url(r'^friends/$', friends),
	url(r'^neighbours/$', neighbours),
	url(r'^blocks/$', blocks),
	url(r'^show/$', show),
	#url(r'^msgsuccess/$', msgsuccess),
	#url(r'^messages/$', messages),
	url(r'^next/$', next),
	url(r'^next/([0-9]*)/$', next),
	url(r'^frequest/([0-9]*)/$', frequest),
	url(r'^togo/([0-9]*)/$', togo),
	url(r'^to/([0-9]*)/$', to),
	url(r'^oo/([0-9]*)/$', oo),
	url(r'^home/homepage/blockthreads/$', blockthreads),
	url(r'^home/homepage/allthreads/$', allthreads),
	url(r'^home/homepage/neighbourhoodthreads/$', neighbourhoodthreads),
	url(r'^home/homepage/neighbourthreads/$', neighbourthreads),
	url(r'^friendthreads/$', friendthreads),
	url(r'^home/ho/msgsuccess/$',messages),
	url(r'^newmsg/$', newmsg),
	url(r'^newms/$', newms),
	url(r'^acceptfrndreq/([0-9]*)$', acceptfrndreq),
	url(r'^sendblkreq/([0-9]*)$', sendblkreq),
	url(r'^acceptblkreq/([0-9]*)$', acceptblkreq),
	url(r'^declinefrndreq/([0-9]*)$', declinefrndreq),
	url(r'^notifications/$', notifications),
	#url(r'^getid/$', getid),
	url(r'^accounts/profile/$', profile),
	
]
