from uuid import uuid4


def get_test_domain():
    """Utility to return a random domain for tests
    """
    return 'example-{uuid}.org'.format(uuid=uuid4().hex)


def get_test_email():
    """Utility to return a random email for tests
    """
    return '{uuid}@mailinator.com'.format(uuid=uuid4().hex)
