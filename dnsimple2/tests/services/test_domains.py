from unittest import skip

from requests.exceptions import HTTPError

from dnsimple2.resources import (
    CollaboratorResource,
    DomainResource,
    EmailForwardResource,
    ResourceList
)
from dnsimple2.resources.domains import PushResource
from dnsimple2.tests.services.base import BaseServiceTestCase
from dnsimple2.tests.utils import (
    get_test_domain_name,
    get_test_email
)


class DomainServiceTests(BaseServiceTestCase):
    @classmethod
    def tearDownClass(cls):
        # TODO: Delete domains created by tests
        pass

    def test_list(self):
        response = self.client.domains.list(self.account)

        self.assertIsInstance(response, ResourceList)
        for item in response:
            self.assertIsInstance(item, DomainResource)

    def test_list_lazy_load(self):
        resources = self.client.domains.list(self.account)
        self.assertIsInstance(resources, ResourceList)

        internal_list = resources._list
        # Load first cached item
        item = resources[0]
        self.assertIsInstance(item, DomainResource)

        # Load last cached item
        item = resources[29]
        self.assertIsInstance(item, DomainResource)
        self.assertEqual(len(internal_list), 30)

        # Lazy load second page
        item = resources[30]
        self.assertIsInstance(item, DomainResource)

        self.assertEqual(len(internal_list), 60)

        # Lazy load fifth page
        item = resources[120]
        self.assertIsInstance(item, DomainResource)

        # We don't have slicing support yet. Thus iterate over a sub-range
        # and do explicit asserts individually.
        for i in range(60, 120):
            self.assertEqual(internal_list[i], None)

        self.assertEqual(len(internal_list), 150)

        # Lazy load third page
        item = resources[60]
        self.assertIsInstance(item, DomainResource)
        self.assertEqual(len(internal_list), 150)

        for i in range(90, 120):
            self.assertEqual(internal_list[i], None)

        self.assertEqual(len(internal_list), 150)

        # Load out of bounds
        with self.assertRaises(IndexError):
            resources[len(resources)]

    def test_create_with_no_data(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.create(self.account, DomainResource(name='', account=self.account))

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
            self.client.domains.create(
                self.account,
                DomainResource(name='invalid-domain', account=self.account)
            )

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
        domain = DomainResource(name=get_test_domain_name(), account=self.account)
        response = self.client.domains.create(self.account, domain)
        self.assertIsInstance(response, DomainResource)
        self.assertEqual(response.name, domain.name)

    def test_get_with_invalid_domain_name(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.get(self.account, self.invalid_domain)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `invalid-domain` not found"
        })

    def test_get_with_valid_domain_name(self):
        response = self.client.domains.get(self.account, self.domain)
        self.assertIsInstance(response, DomainResource)
        self.assertEqual(response.name, self.domain.name)

    def test_delete_for_invalid_domain(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.delete(self.account, self.invalid_domain)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `invalid-domain` not found"
        })

    def test_delete_with_valid_data(self):
        # We cannot use self.domain here because other tests need it that
        # will run after this.
        domain = self.client.domains.create(
            self.account,
            DomainResource(name=get_test_domain_name(), account=self.account)
        )
        response = self.client.domains.delete(self.account, domain)
        self.assertIsNone(response)

    def test_reset_token_with_invalid_domain(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.reset_token(self.account, self.invalid_domain)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `invalid-domain` not found"
        })

    def test_reset_token_with_valid_domain(self):
        response = self.client.domains.reset_token(self.account, self.domain)
        self.assertIsInstance(response, DomainResource)
        self.assertEqual(self.domain.id, response.id)
        self.assertEqual(self.domain.account.id, response.account.id)
        self.assertEqual(self.domain.name, response.name)
        self.assertNotEqual(self.domain.token, response.token)


class CollaboratorServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(CollaboratorServiceTests, cls).setUpClass()

        cls.collaborator = cls.client.domains.collaborators.add(
            cls.domain,
            CollaboratorResource(user_email=get_test_email())
        )

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
            self.client.domains.collaborators.add(
                self.invalid_domain,
                CollaboratorResource(user_email=get_test_email())
            )

        exception = e.exception
        self.assertEqual(exception.response.status_code, 404)
        self.assertEqual(exception.response.json(), {
            "message": "Domain `1` not found"
        })

    def test_add_collaborators_for_valid_domain(self):
        email = get_test_email()
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
        cls.invalid_domain = DomainResource(id=1, account=cls.account)

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


class PushServiceTests(BaseServiceTestCase):
    @classmethod
    def setUpClass(cls):
        super(PushServiceTests, cls).setUpClass()
        cls.push = cls.client.domains.pushes.add(
            cls.domain,
            PushResource(new_account_email='at.mishra007@gmail.com')
        )

    def test_list_push_for_invalid_account(self):
        with self.assertRaises(HTTPError) as e:
            self.client.domains.pushes.list(self.invalid_account)

        exception = e.exception
        self.assertEqual(exception.response.status_code, 401)

    def test_list_push_for_valid_account(self):
        response = self.client.domains.pushes.list(self.account)
        self.assertIsInstance(response, list)
        for item in response:
            self.assertIsInstance(item, PushResource)
