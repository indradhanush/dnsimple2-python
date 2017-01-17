from dnsimple2.resources import DomainResource
from dnsimple2.tests.services.base import BaseServiceTestCase


class DomainServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(DomainServiceTests, cls).setUpClass()
        cls.domains = cls.client.domains

    def test_get(self):
        response = self.domains.get(424)
        for item in response:
            self.assertIsInstance(item, DomainResource)
