import os
from unittest import TestCase

from dnsimple2.client import DNSimple
from dnsimple2.resources import (
    AccountResource,
    DomainResource
)
from dnsimple2.tests.utils import get_test_domain_name


class BaseServiceTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        access_token = os.getenv('DNSIMPLE_V2_ACCESS_TOKEN')
        cls.client = DNSimple(access_token)

        account_id = os.getenv('DNSIMPLE_ACCOUNT_ID')
        cls.account = AccountResource(id=account_id)
        cls.domain = cls.client.domains.create(
            cls.account,
            DomainResource(name=get_test_domain_name(), account=cls.account)
        )
        cls.invalid_domain = DomainResource(
            id=1,
            name='invalid-domain',
            account=cls.account
        )
