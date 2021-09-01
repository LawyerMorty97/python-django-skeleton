from django.http import HttpRequest

from threading import local


_thread_locals = local()


def get_request_domain(request: HttpRequest) -> str:
    scheme = request.scheme
    host = request.get_host()
    return "{}://{}".format(scheme, host)


def set_current_request(request):
    _thread_locals.current_request = request


def get_current_request():
    return getattr(_thread_locals, "current_request", None)
