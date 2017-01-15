class BaseService(object):
    def __init__(self, client, identifier):
        self.client = client
        self.url = '{base_url}{identifier}'.format(
            base_url=self.client.api_url,
            identifier=identifier
        )
