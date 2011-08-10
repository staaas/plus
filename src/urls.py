from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'src.views.home', name='home'),
    # url(r'^src/', include('src.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^soc/', include('social_auth.urls')),
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
