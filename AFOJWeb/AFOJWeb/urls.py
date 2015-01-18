from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AFOJWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','oj.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns+=patterns((''),
	(r'^account/',include('account.urls')),
	)

urlpatterns+=patterns((''),
	(r'^problemlist/',include('problemlist.urls')),
	)

urlpatterns+=patterns((''),
	(r'^contest/',include('status.urls')),
	)

urlpatterns+=patterns((''),
	(r'^status/',include('status.urls')),
	)

urlpatterns+=patterns((''),
	(r'^blog/',include('blog.urls')),
	)

urlpatterns+=patterns((''),
	(r'^discuss/',include('discuss.urls')),
	)

urlpatterns+=patterns((''),
	(r'^userinfo/',include('userinfo.urls')),
	)

urlpatterns+=patterns((''),
	(r'^wiki/',include('wiki.urls')),
	)

urlpatterns+=patterns((''),
	(r'^game/',include('game.urls')),
	)

urlpatterns+=patterns((''),
	(r'^dashboard/',include('dashboard.urls')),
	)

