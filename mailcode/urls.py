from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings;
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
#    url(r'^$', 'puck.views.home', name='home'),
    # url(r'^puck/', include('puck.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^statd/(?P<q_type>.*)', 'statd.views.statd'),
    url(r'^search/', 'task.views.search'),
    url(r'^analyse/(?P<branch_id>.*)/(?P<client_id>.*)/(?P<message_ids>.*)/(?P<domain>.*)/(?P<subject>.*)/$', 'analyse.analyse-views.analyse'),
    url(r'^/static/(?P<path>.*)$','django.views.static.serve',  {'document_root' : settings.STATIC_DIR}),
)
