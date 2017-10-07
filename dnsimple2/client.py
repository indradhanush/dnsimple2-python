from cached_property import cached_property
import requests

from dnsimple2.services import (
    AccountService,
    CertificateService,
    DomainService,
    WhoAmIService,
)


class DNSimple(object):
    def __init__(self, access_token, test_mode=True):
        self._session = None
        self._set_url(test_mode)

        self.authentication = {
            'Authorization': 'Bearer {access_token}'.format(access_token=access_token)
        }

        self.whoami = WhoAmIService(self)
        self.accounts = AccountService(self)
        self.domains = DomainService(self)
        self.certificates = CertificateService(self)

    def _set_url(self, test_mode=True):
        if test_mode:
            self.api_url = 'https://api.sandbox.dnsimple.com/v2/'
        else:
            self.api_url = 'https://api.dnsimple.com/v2/'

    @cached_property
    def session(self):
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(**self.authentication)
            self._session.headers.update({
                'Accept': 'application/json'
            })

        return self._session

    def get(self, url, **kwargs):
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    def post(self, url, data={}):
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json()

    def delete(self, url):
        response = self.session.delete(url)
        response.raise_for_status()
