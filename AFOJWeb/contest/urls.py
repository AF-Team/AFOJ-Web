from django.conf.urls import *
urlpatterns=patterns('contest.views',
	url(r'^$','contest_list'),
	)
