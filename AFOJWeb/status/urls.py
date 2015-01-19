from django.conf.urls import *
urlpatterns=patterns('status.views',
	url(r'^$','index'),
	url(r'^code$','code_show')
	)
