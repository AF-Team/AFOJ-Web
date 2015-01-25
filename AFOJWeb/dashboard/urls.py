from django.conf.urls import *
urlpatterns=patterns('dashboard.views',
	url(r'^$','index'),
	url(r'^problem$','dashboard_problem'),
	url(r'^addproblem$','dashboard_add_problem'),
	url(r'^contest$','dashboard_contest'),
	url(r'^addcontest$','dashboard_add_contest'),
	url(r'^fps$','fps_upload'),
	url(r'^addnews$','dashboard_add_news'),
	url(r'^news','dashboard_news')

	)
