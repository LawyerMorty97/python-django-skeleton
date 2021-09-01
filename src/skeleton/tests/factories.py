import uuid
import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from django.contrib.auth.models import Group
from django.utils.text import slugify

faker = FakerFactory.create("EN")
