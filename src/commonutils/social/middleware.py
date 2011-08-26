from .socialize import socialize_user

class LazySocialUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            from django.contrib.auth import get_user
            request._cached_user = socialize_user(get_user(request))
        return request._cached_user


class SocialAuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.__class__.user = LazySocialUser()
        return None
