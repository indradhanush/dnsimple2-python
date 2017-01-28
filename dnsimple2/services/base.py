class BaseService(object):
    def __init__(self, client, endpoint):
        self.client = client
        self.url = '{base_url}{endpoint}'.format(
            base_url=self.client.api_url,
            endpoint=endpoint
        )
