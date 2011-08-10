# -*- coding:utf-8 -*-
from functools import wraps

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation


def render_to(template):
    """
    Decorator for compact calling views
    """
    def renderer(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            response = func(request, *args, **kwargs)

            if isinstance(response, dict):
                lang = response.pop('Content-Language', None)
                resp = render_to_response(template, response, context_instance=RequestContext(request))
                if not lang is None:
                    resp['Content-Language'] = lang
                    translation.deactivate()
                return resp
            else:
                return response
        return wrapper
    return renderer
