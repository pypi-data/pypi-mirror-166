#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement

import uuid
from django.conf import settings
from django_middleware_global_request.middleware import get_request

DJANGO_REQUEST_ID_ATTRIBUTE = getattr(settings, "DJANGO_REQUEST_ID_ATTRIBUTE", "_request_id")
DJANGO_REQUEST_ID_HEADER = getattr(settings, "DJANGO_REQUEST_ID_HEADER", "HTTP_X_REQUEST_ID")

class DjangoMiddlewareRequestId(object):

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request_id = request.META.get("HTTP_X_REQUEST_ID", None)
        if not request_id:
            request_id = uuid.uuid4().hex
        setattr(request, DJANGO_REQUEST_ID_ATTRIBUTE, request_id)
        response = self.get_response(request)
        return response


def get_request_id():
    request = get_request()
    return getattr(request, DJANGO_REQUEST_ID_ATTRIBUTE, "")
