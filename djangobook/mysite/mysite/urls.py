from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from mysite.views import *
from books.views import *
from cookies.views import *
from contact.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^meta/$', display_meta),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
#    url(r'^search-form/$', search_form),
    url(r'^search/$', search),
    url(r'^contact/thanks/$', 'contact.views.thanks'),
    url(r'^contact/$', contact),
    url(r'^cookie/$', show_color),
    url(r'^set_cookie/$', set_color),
)

#if settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^debuginfo/$', 'mysite.views.debug'),
#    )
