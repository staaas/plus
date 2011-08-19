from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from social_auth.views import complete


admin.autodiscover()

if settings.DEBUG:
    urlpatterns = patterns('', (r'^site_media/media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),)
    urlpatterns += patterns('', (r'^site_media/static/(?P<path>.*)$',
                                 'django.views.static.serve',
                                 {'document_root': settings.STATIC_ROOT}),)
else:
    urlpatterns = []

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'src.views.home', name='home'),
    # url(r'^src/', include('src.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^soc/', include('social_auth.urls')),
    url(r'^soc/complete/(?P[^/]+)/$', csrf_exempt(complete), name='complete'),
    url(r'^$', 'plus.views.home', name='home'),
    url(r'^(?P<slug>[\w\d]+)/$',
        'plus.views.show_event',
        name='show_event'),
    url(r'^(?P<slug>[\w\d]+)/plus/',
        'plus.views.event_plus',
        name='event_plus'),
    url(r'^(?P<slug>[\w\d]+)/minus/',
        'plus.views.event_minus',
        name='event_minus'),
    url(r'^(?P<slug>[\w\d]+)/logout/',
        'plus.views.event_logout',
        name='event_logout'),
)
