from django.conf.urls import *
urlpatterns=patterns('status.views',
	url(r'^$','index'),
	url(r'^contest$','contest_status_list'),
	url(r'^code$','code_show')
	)
