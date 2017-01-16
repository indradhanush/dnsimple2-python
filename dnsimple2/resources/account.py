from dateutil.parser import parse

from dnsimple2.resources.base import BaseResource


class AccountResource(BaseResource):
    fields = ('id', 'email', 'plan_identifier', 'created_at', 'updated_at',)

    def __init__(self, data):
        if data is None:
            return

        self.id = data.get('id')
        self.email = data.get('email')
        self.plan_identifier = data.get('plan_identifier')
        self.created_at = parse(data.get('created_at'))
        self.updated_at = parse(data.get('updated_at'))
