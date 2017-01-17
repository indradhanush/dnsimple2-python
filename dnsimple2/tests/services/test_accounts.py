from dnsimple2.resources import AccountResource
from dnsimple2.tests.services.base import BaseServiceTestCase


class AccountServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(AccountServiceTests, cls).setUpClass()
        cls.accounts = cls.client.accounts

    def test_get(self):
        response = self.accounts.get()
        self.assertIsInstance(response, list)

        for item in response:
            self.assertIsInstance(item, AccountResource)
