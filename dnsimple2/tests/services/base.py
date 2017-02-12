import os
from unittest import TestCase

from dnsimple2.client import DNSimple
from dnsimple2.resources import AccountResource


class BaseServiceTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        access_token = os.getenv('DNSIMPLE_V2_ACCESS_TOKEN')
        cls.client = DNSimple(access_token)
        cls.account = AccountResource(id=424)
