from dnsimple2 import resources, services


class CertificateService(services.BaseService):
    def __init__(self, client):
        super().__init__(
            client=client,
            endpoint='{account_id}/domains/{domain_id}/certificates',
        )

    def get_url(self, account, domain, certificate_id=None):
        url = self.url.format(
            account_id=account.id,
            domain_id=domain.id,
        )

        if certificate_id:
            url += '/{certificate_id}'.format(certificate_id=certificate_id)

        return url

    def _list(self, account, domain, page):
        response = self.client.get(
            self.get_url(account, domain),
            data={'page': page},
        )
        return [
            resources.CertificateResource(**item)
            for item in response['data']
        ], response['pagination']

    def list(self, account, domain, page=1):
        certificates, pagination = self._list(account, domain, page)

        resource_list = resources.ResourceList(
            self,
            pagination['total_entries'],
            pagination['per_page'],
            [account, domain]
        )
        resource_list.update(certificates, page)
        return resource_list

    def get(self, account, domain, certificate_id):
        response = self.client.get(self.get_url(
            account, domain, certificate_id=certificate_id,
        ))
        return resources.CertificateResource(**response['data'])

    def download(self, account, domain, certificate_id):
        response = self.client.get(self.get_url(
            account, domain, certificate_id=certificate_id,
        ) + "/download")
        return resources.DownloadedCertificateResource(**response['data'])

    def get_private_key(self, account, domain, certificate_id):
        return self.client.get(self.get_url(
            account, domain, certificate_id=certificate_id,
        ) + "/private_key")['data']['private_key']
