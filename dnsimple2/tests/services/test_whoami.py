from dnsimple2.resources import (
    AccountResource,
    UserResource,
    WhoAmIResource
)
from dnsimple2.tests.services.base import BaseServiceTestCase


class WhoAmIServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(WhoAmIServiceTests, cls).setUpClass()
        cls.whoami = cls.client.whoami

    def test_get(self):
        response = self.whoami.get()
        self.assertIsInstance(response, WhoAmIResource)

        self.assertIsInstance(response.user, UserResource)
        for field in response.user.fields:
            self.assertIsNotNone(getattr(response.user, field))

        self.assertIsInstance(response.account, AccountResource)
