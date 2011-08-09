# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from functools import wraps

def render_to(template):
    """
    Decorator for compact calling views
    """
    def renderer(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            response = func(request, *args, **kwargs)

            if isinstance(response, dict):
                return render_to_response(template, response, context_instance=RequestContext(request))
            else:
                return response
        return wrapper
    return renderer
