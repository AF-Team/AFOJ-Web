from django.conf.urls import *
urlpatterns=patterns('contest.views',
	url(r'^$','contest_list'),
	url(r'^contest$','contest_problem_list'),
	)
