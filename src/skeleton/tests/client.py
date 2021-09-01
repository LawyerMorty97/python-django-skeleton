from django.test.client import Client as DjangoTestClient

_MISSING = object()
_APPLICATION_JSON = "application/json"


class JsonClient(DjangoTestClient):
    """
    Test client subclass that uses "application/json"
    as content type by default
    """

    def post(self, *args, content_type=_MISSING, **kwargs):
        if content_type is _MISSING:
            content_type = _APPLICATION_JSON

        return super().post(*args, content_type=content_type, **kwargs)

    def put(self, *args, content_type=_MISSING, **kwargs):
        if content_type is _MISSING:
            content_type = _APPLICATION_JSON

        return super().put(*args, content_type=content_type, **kwargs)

    def patch(self, *args, content_type=_MISSING, **kwargs):
        if content_type is _MISSING:
            content_type = _APPLICATION_JSON

        return super().patch(*args, content_type=content_type, **kwargs)
