from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

handler500 = 'plus.views.error500'

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

    url(r'^soc/login/(?P<backend>[^/]+)/$',
        'plus.views.plus_socialauth_begin',
        name='plus_socialauth_begin'),
    url(r'^soc/', include('social_auth.urls')),
    url(r'^auth-error/$', 'plus.views.auth_error', name='error'),
    url(r'^$', 'plus.views.home', name='home'),

    url(r'^(?P<url>[\w\d/]*)logout/',
        'plus.views.anything_logout',
        name='anything_logout'),
    url(r'^(?P<slug>[\w\d]+)/$',
        'plus.views.show_event',
        name='show_event'),
    url(r'^(?P<slug>[\w\d]+)/plus/',
        'plus.views.event_plus',
        name='event_plus'),
    url(r'^(?P<slug>[\w\d]+)/minus/',
        'plus.views.event_minus',
        name='event_minus'),
)
