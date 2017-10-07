from dnsimple2 import resources, services


class CertificateService(services.BaseService):
    def __init__(self, client):
        super().__init__(
            client=client,
            endpoint='{account_id}/domains/{domain_id}/certificates',
        )

    def get_url(self, account, domain, certificate=None):
        url = self.url.format(
            account_id=account.id,
            domain_id=domain.id,
        )

        if certificate:
            url += '/{certificate_id}'.format(certificate_id=certificate.id)

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
