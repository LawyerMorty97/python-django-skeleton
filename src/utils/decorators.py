from functools import wraps
from django.db import transaction


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get("raw"):
            return
        signal_handler(*args, **kwargs)

    return wrapper


def on_transaction_commit(f):
    def handle(*args, **kwargs):
        transaction.on_commit(lambda: f(*args, **kwargs))

    return handle
