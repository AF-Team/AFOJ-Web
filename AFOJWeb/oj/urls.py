from django.conf.urls import *
urlpatterns=patterns('oj.views',
	url(r'^news$','news_list_show'),
	url(r'^news/(?P<nid>\d+)$','news_show'),
	url(r'^submit$','submit_code'),
	)
