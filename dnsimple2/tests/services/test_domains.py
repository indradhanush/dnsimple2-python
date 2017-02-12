from unittest import skip
from uuid import uuid4

from requests.exceptions import HTTPError

from dnsimple2.resources import (
    CollaboratorResource,
    DomainResource,
    EmailForwardResource
)
from dnsimple2.tests.services.base import BaseServiceTestCase
from dnsimple2.tests.utils import (
    get_test_domain,
    get_test_email
)


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
            self.client.domains.create(424, data=None)

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
            self.client.domains.create(424, dict(name='invalid-domain'))

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
            self.client.domains.get(424, 'invalid-domain')

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

    def test_delete_for_invalid_domain(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.delete(424, 'invalid-domain')

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `invalid-domain` not found"
        })

    def test_delete_with_valid_data(self):
        # We cannot use self.domain here because the `get` tests use it.
        domain = 'example-{uuid}.org'.format(uuid=uuid4().hex)
        self.client.domains.create(424, dict(name=domain))

        response = self.client.domains.delete(424, domain)
        self.assertIsNone(response)

    def test_reset_token_with_invalid_domain(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.reset_token(424, 'invalid-domain')

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `invalid-domain` not found"
        })

    def test_reset_token_with_valid_domain(self):
        name = 'example-{uuid}.org'.format(uuid=uuid4().hex)
        domain = self.client.domains.create(424, dict(name=name))

        response = self.client.domains.reset_token(424, domain.name)
        self.assertIsInstance(response, DomainResource)
        self.assertEqual(domain.id, response.id)
        self.assertEqual(domain.account_id, response.account_id)
        self.assertEqual(domain.name, response.name)
        self.assertNotEqual(domain.token, response.token)


class CollaboratorServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(CollaboratorServiceTests, cls).setUpClass()
        name = 'example-{uuid}.org'.format(uuid=uuid4().hex)
        cls.domain = cls.client.domains.create(424, dict(name=name))

        email = '{uuid}@mailinator.com'.format(uuid=uuid4().hex)
        cls.collaborator = cls.client.domains.collaborators.add(
            cls.domain,
            CollaboratorResource(user_email=email)
        )
        cls.invalid_domain = DomainResource(id=1, account_id=424)

    def test_list_collaborators_for_invalid_domain(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.collaborators.list(self.invalid_domain)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `1` not found"
        })

    def test_list_collaborators_for_valid_domain(self):
        response = self.client.domains.collaborators.list(self.domain)
        self.assertIsInstance(response, list)
        for item in response:
            self.assertIsInstance(item, CollaboratorResource)

    def test_add_collaborators_for_invalid_domain(self):
        with self.assertRaises(HTTPError) as e:
            email = '{uuid}@mailinator.com'.format(uuid=uuid4().hex)
            self.client.domains.collaborators.add(
                self.invalid_domain,
                CollaboratorResource(user_email=email)
            )

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `1` not found"
        })

    def test_add_collaborators_for_valid_domain(self):
        email = '{uuid}@mailinator.com'.format(uuid=uuid4().hex)
        response = self.client.domains.collaborators.add(
            self.domain, CollaboratorResource(user_email=email)
        )
        self.assertIsInstance(response, CollaboratorResource)
        self.assertEqual(response.user_email, email)

    def test_delete_collaborator_for_valid_domain(self):
        # Currently the API returns a 500 even though the collaborator is
        # deleted. Our tests will match that, so when this is fixed on
        # DNSimple, our tests start failing and we will take notice.
        with self.assertRaises(HTTPError) as e:
            self.client.domains.collaborators.delete(self.domain, self.collaborator)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 500)


@skip('Creating an email forward is throwing a 500 currently')
class EmailForwardServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(EmailForwardServiceTests, cls).setUpClass()

        cls.domain = cls.client.domains.create(424, dict(name=get_test_domain()))
        cls.invalid_domain = DomainResource(id=1, account_id=424)

        email_forward = EmailForwardResource(
            from_email=get_test_email(),
            to=get_test_email()
        )
        cls.email_forward = cls.client.domains.email_forwards.create(cls.domain, email_forward)

    def test_list_email_forwards_for_invalid_domain(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.email_forwards.list(self.invalid_domain)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `1` not found"
        })

    def test_list_email_forwards_for_valid_domain(self):
        response = self.client.domains.email_forwards.list(self.domain)
        self.assertIsInstance(response, list)
        for item in response:
            self.assertIsInstance(item, EmailForwardResource)

    def test_get_with_invalid_email_forwards(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.email_forwards.get(
                self.domain,
                EmailForwardResource(id=1)
            )
        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Email forward `1` not found"
        })

    def test_get_with_valid_email_forwards(self):
        response = self.client.domains.email_forwards.get(self.domain, self.email_forward)
        self.assertIsInstance(response, EmailForwardResource)
        self.assertEqual(response.id, self.email_forward.id)
        self.assertEqual(response.from_email, self.email_forward.from_email)
        self.assertEqual(response.to, self.email_forward.to)
