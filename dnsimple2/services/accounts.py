from dnsimple2.resources import AccountResource
from dnsimple2.services import BaseService


class AccountService(BaseService):
    def __init__(self, client):
        super(AccountService, self).__init__(
            client=client,
            endpoint='accounts'
        )

    def get(self):
        response = self.client.get(self.url)
        return [AccountResource(**item) for item in response['data']]
