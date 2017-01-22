from dnsimple2.resources import DomainResource
from dnsimple2.services import BaseService


class DomainService(BaseService):
    def __init__(self, client):
        super(DomainService, self).__init__(client, '{account_id}/domains')

    def get_url(self, account_id):
        return self.url.format(account_id=account_id)

    def get(self, account_id, **kwargs):
        response = self.client.get(self.get_url(account_id), **kwargs)
        return [DomainResource(item) for item in response['data']]

    def create(self, account_id, data):
        response = self.client.post(self.get_url(account_id), data)
        return DomainResource(response['data'])
