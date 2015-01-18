from django.conf.urls import *
urlpatterns=patterns('problemlist.views',
	url(r'^$','index'),
	url(r'^problem/(?P<pid>\d{4})/$','problem_show'),
	)
