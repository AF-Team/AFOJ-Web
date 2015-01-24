from django.conf.urls import *
urlpatterns=patterns('userinfo.views',
	url(r'^$','index'),
	url(r'^(?P<username>\w+)$','userinfo')
	)
