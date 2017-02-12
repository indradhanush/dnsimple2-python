from dateutil.parser import parse

from dnsimple2.resources.base import BaseResource


class AccountResource(BaseResource):
    fields = ('id', 'email', 'plan_identifier', 'created_at', 'updated_at',)

    def __init__(self, **kwargs):
        if kwargs is None:
            return

        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        self.plan_identifier = kwargs.get('plan_identifier')
        self.created_at = parse(kwargs.get('created_at'))
        self.updated_at = parse(kwargs.get('updated_at'))
