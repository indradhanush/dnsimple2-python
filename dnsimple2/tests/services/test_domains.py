from uuid import uuid4

from requests.exceptions import HTTPError

from dnsimple2.resources import DomainResource
from dnsimple2.tests.services.base import BaseServiceTestCase


class DomainServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(DomainServiceTests, cls).setUpClass()
        cls.domain = 'example-{uuid}.org'.format(uuid=uuid4().hex)

    @classmethod
    def tearDownClass(cls):
        # TODO: Delete domains created by tests
        pass

    def test_list(self):
        response = self.client.domains.list(424)
        for item in response:
            self.assertIsInstance(item, DomainResource)

    def test_create_with_no_data(self):
        with self.assertRaises(HTTPError) as e:
            response = self.client.domains.create(424, data=None)
            self.assertIsNone(response)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 400)
        self.assertEqual(exception.response.json(), {
            'message': 'Validation failed',
            'errors': {
                'name': ["can't be blank", 'is an invalid domain']
                }
            }
        )

    def test_create_with_invalid_data(self):
        with self.assertRaises(HTTPError) as e:
            response = self.client.domains.create(424, dict(name='invalid-domain'))
            self.assertIsNone(response)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 400)
        self.assertEqual(exception.response.json(), {
            'message': 'Validation failed',
            'errors': {
                'name': ['is an invalid domain']
                }
            }
        )

    def test_create_with_valid_data(self):
        response = self.client.domains.create(424, dict(name=self.domain))
        self.assertIsInstance(response, DomainResource)

    def test_get_with_invalid_domain_name(self):
        with self.assertRaises(HTTPError) as e:
            response = self.client.domains.get(424, 'invalid-domain')
            self.assertIsNone(response)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `invalid-domain` not found"
        })

    def test_get_with_valid_domain_name(self):
        # test_create will execute before this, thus self.domain will be available
        response = self.client.domains.get(424, self.domain)
        self.assertIsInstance(response, DomainResource)
        self.assertEqual(response.name, self.domain)
