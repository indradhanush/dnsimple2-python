from dnsimple2.resources.base import BaseResource


class DomainResource(BaseResource):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.account_id = kwargs.get('account_id')
        self.registrant_id = kwargs.get('registrant_id')
        self.name = kwargs.get('name')
        self.unicode_name = kwargs.get('unicode_name')
        self.token = kwargs.get('token')
        self.state = kwargs.get('state')
        self.auto_renew = kwargs.get('auto_renew')
        self.private_whois = kwargs.get('private_whois')
        self.expires_on = self.parse_datetime(kwargs.get('expires_on'))
        self.created_at = self.parse_datetime(kwargs.get('created_at'))
        self.updated_at = self.parse_datetime(kwargs.get('updated_at'))


class CollaboratorResource(BaseResource):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.domain_id = kwargs.get('domain_id')
        self.domain_name = kwargs.get('domain_name')
        self.user_id = kwargs.get('user_id')
        self.user_email = kwargs.get('user_email')
        self.invitation = kwargs.get('invitation')
        self.created_at = self.parse_datetime(kwargs.get('created_at'))
        self.updated_at = self.parse_datetime(kwargs.get('updated_at'))
        self.accepted_at = self.parse_datetime(kwargs.get('accepted_at'))


class EmailForwardResource(BaseResource):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.domain_id = kwargs.get('domain_id')
        self.from_email = kwargs.get('from_email')
        self.to = kwargs.get('to')
        self.created_at = self.parse_datetime(kwargs.get('created_at'))
        self.updated_at = self.parse_datetime(kwargs.get('updated_at'))
