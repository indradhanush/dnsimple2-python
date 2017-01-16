from dnsimple2.resources import AccountResource
from dnsimple2.services import BaseService


class AccountsService(BaseService):
    def __init__(self, client):
        super(AccountsService, self).__init__(client, 'accounts')

    def get(self):
        response = self.client.get(self.url)
        return [AccountResource(item) for item in response]
