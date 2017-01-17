from dateutil.parser import parser

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

        expires_on = data.get('expires_on')
        if expires_on is not None:
            self.expires_on = parser.parse(expires_on) if expires_on else None

        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
