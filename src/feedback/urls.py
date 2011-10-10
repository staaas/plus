from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('feedback.views',
    url(r'^$', 'submit_feedback', name='submit_feedback'),
)
