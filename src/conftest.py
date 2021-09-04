import logging
import pytest
import json
import random
import string
from unittest import mock
import requests

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model

from skeleton.tests.factories import *  # noqa
from skeleton.tests.client import JsonClient, DjangoTestClient

pytestmark = pytest.mark.django_db

UserModel = get_user_model()


@pytest.fixture(autouse=True)
def disable_console_logger(settings):
    """
    Removes the "console" handler from the root logger,
    so pytest doesn't log everything twice
    """
    logger = logging.getLogger("")
    stream_handler = None
    for handler in logger.handlers:
        if type(handler) == logging.StreamHandler:
            stream_handler = handler
            break

    if stream_handler:
        logger.removeHandler(handler)
        yield
        logger.addHandler(handler)
    else:
        yield


@pytest.fixture(autouse=True)
def use_default_staticfiles_storage_in_tests(settings):
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )


@pytest.fixture  # noqa: C901 -0 ignore "too complex"
def asserts():
    class Asserts:
        @staticmethod
        def assert_response_keys_equal(response, keys, msg=None):
            data = json.loads(response.content)
            if msg:
                assert set(data.keys()) == set(keys), msg
            else:
                assert set(data.keys()) == set(keys)

        @staticmethod
        def assert_mutually_exclusive(list1, list2, attr_path):
            def get_nested_attr(obj, path):
                attr_keys = path.split(".")
                nested_attr = obj
                for k in attr_keys:
                    if k in nested_attr:
                        nested_attr = nested_attr.get(k)
                    else:
                        nested_attr = None
                        break
                return nested_attr

            set1 = set([get_nested_attr(x, attr_path) for x in list1])
            set2 = set([get_nested_attr(x, attr_path) for x in list2])

            assert not set1.intersection(set2)

    return Asserts


@pytest.fixture
def vanilla_client(user):
    return JsonClient()


@pytest.fixture
def user(db):
    return UserModel.objects.create(
        email="test@skeleton.org", first_name="Test", last_name="Testersen"
    )
