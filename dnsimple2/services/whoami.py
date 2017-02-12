from dnsimple2.resources import WhoAmIResource
from dnsimple2.services import BaseService


class WhoAmIService(BaseService):
    def __init__(self, client):
        super(WhoAmIService, self).__init__(client, 'whoami')

    def get(self):
        response = self.client.get(self.url)
        return WhoAmIResource(**response['data'])
