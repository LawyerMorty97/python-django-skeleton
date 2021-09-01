import logging

from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, Http404
from django.conf import settings
from utils.request import get_request_domain, set_current_request
from utils.debug import QueryCounter

logger = logging.getLogger(__name__)


def db_query_count_middleware(get_response):
    def middleware(request):
        with QueryCounter("request", print=True):
            response = get_response(request)

        return response

    return middleware


def check_domain_middleware(get_response):
    def middleware(request):
        request_domain = get_request_domain(request)

        return get_response(request)

    return middleware
