from django.conf.urls import *
urlpatterns=patterns('account.views',
	url(r'^$','sign_in'),
	url(r'^signup$','sign_up'),
	url(r'^logout$','log_out'),
	)
