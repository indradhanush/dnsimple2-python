from dnsimple2.resources.base import BaseResource


class DomainResource(BaseResource):
    def __init__(self, data):
        self.id = data.get('id')
        self.account_id = data.get('account_id')
        self.registrant_id = data.get('registrant_id')
        self.name = data.get('name')
        self.unicode_name = data.get('unicode_name')
        self.token = data.get('token')
        self.state = data.get('state')
        self.auto_renew = data.get('auto_renew')
        self.private_whois = data.get('private_whois')
        self.expires_on = self.parse_datetime(data.get('expires_on'))
        self.created_at = self.parse_datetime(data.get('created_at'))
        self.updated_at = self.parse_datetime(data.get('updated_at'))


class CollaboratorResource(BaseResource):
    def __init__(self, data):
        self.id = data.get('id')
        self.domain_id = data.get('domain_id')
        self.domain_name = data.get('domain_name')
        self.user_id = data.get('user_id')
        self.user_email = data.get('user_email')
        self.invitation = data.get('invitation')
        self.created_at = self.parse_datetime(data.get('created_at'))
        self.updated_at = self.parse_datetime(data.get('updated_at'))
        self.accepted_at = self.parse_datetime(data.get('accepted_at'))


class EmailForwardResource(BaseResource):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.domain_id = kwargs.get('domain_id')
        self.from_email = kwargs.get('from_email')
        self.to = kwargs.get('to')
        self.created_at = self.parse_datetime(kwargs.get('created_at'))
        self.updated_at = self.parse_datetime(kwargs.get('updated_at'))
