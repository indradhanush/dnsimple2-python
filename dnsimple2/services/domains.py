from dnsimple2.resources import (
    CollaboratorResource,
    DomainResource,
    EmailForwardResource,
    PushResource,
    ResourceList
)

from dnsimple2.services import BaseService


class DomainService(BaseService):
    def __init__(self, client):
        super(DomainService, self).__init__(
            client=client,
            endpoint='{account_id}/domains'
        )
        self.collaborators = CollaboratorService(self)
        self.email_forwards = EmailForwardService(self)
        self.pushes = PushService(self)

    def get_url(self, account, domain=None):
        url = self.url.format(account_id=account.id)
        if domain is not None:
            return url + '/{name}'.format(name=domain.name or domain.id)

        return url

    def _list(self, account, page):
        """Private method. This is also used by ResourceList to get a bare list of
           DomainResource objects
        """
        response = self.client.get(self.get_url(account), data={"page": page})
        return [
            DomainResource(**item) for item in response['data']
        ], response['pagination']

    def list(self, account, page=1):
        resources, pagination = self._list(account, page)

        resource_list = ResourceList(
            self,
            pagination['total_entries'],
            pagination['per_page'],
            [account]
        )
        resource_list.update(resources, page)
        return resource_list

    def get(self, account, domain):
        response = self.client.get(self.get_url(account, domain))
        return DomainResource(**response['data'])

    def create(self, account, domain):
        response = self.client.post(self.get_url(account), dict(name=domain.name))
        return DomainResource(**response['data'])

    def delete(self, account, domain):
        self.client.delete(self.get_url(account, domain))

    def reset_token(self, account, domain):
        url = self.get_url(account, domain) + "/token"
        response = self.client.post(url)
        return DomainResource(**response['data'])


class CollaboratorService(BaseService):
    def __init__(self, domains):
        super(CollaboratorService, self).__init__(
            client=domains.client,
            endpoint='{account_id}/domains/{domain_id}/collaborators'
        )
        self.domains = domains

    def get_url(self, domain, collaborator=None):
        url = self.url.format(account_id=domain.account.id, domain_id=domain.id)
        if collaborator is not None:
            return url + '/{collaborator_id}'.format(collaborator_id=collaborator.id)

        return url

    def list(self, domain):
        response = self.client.get(self.get_url(domain))
        return [CollaboratorResource(**item) for item in response['data']]

    def add(self, domain, collaborator):
        response = self.client.post(self.get_url(domain), {
            'email': collaborator.user_email
        })
        return CollaboratorResource(**response['data'])

    def delete(self, domain, collaborator):
        self.client.delete(self.get_url(domain, collaborator))


class EmailForwardService(BaseService):
    def __init__(self, domain_service):
        super(EmailForwardService, self).__init__(
            client=domain_service.client,
            endpoint='{account_id}/domains/{domain_id}/email_forwards'
        )

    def get_url(self, domain, email_forward=None):
        url = self.url.format(account_id=domain.account.id, domain_id=domain.id)
        if email_forward is not None:
            return url + '/{email_forward_id}'.format(email_forward_id=email_forward.id)

        return url

    def list(self, domain):
        response = self.client.get(self.get_url(domain))
        return [EmailForwardResource(**item) for item in response['data']]

    def get(self, domain, email_forward):
        response = self.client.get(self.get_url(domain, email_forward))
        return EmailForwardResource(**response['data'])

    def create(self, domain, email_forward):
        response = self.client.post(self.get_url(domain), {
            'from': email_forward.from_email,
            'to': email_forward.to
        })
        return EmailForwardResource(**response['data'])

    def delete(self, domain, email_forward):
        self.client.delete(self.get_url(domain, email_forward))

class PushService(BaseService):

    def __init__(self, domains):
        super(PushService, self).__init__(
            client=domains.client,
            endpoint='{account_id}/pushes'
        )
        self.domains = domains
        self.add_endpoint = '{account_id}/domains/{domain_id}/pushes'

    def get_url(self, account, push=None):
        url = self.url.format(account_id=account.id)
        if push is not None:
            return url + '/{push_id}'.format(push_id=push.id)

        return url

    def get_url_for_add(self, domain):
        url = ('{base_url}'+self.add_endpoint).format(base_url = self.domains.client.api_url,
                                                      account_id = domain.account.id,
                                                      domain_id = domain.id)
        return url

    def list(self, account):
        response = self.client.get(self.get_url(account))
        return [PushResource(**item) for item in response['data']]

    def add(self, domain, push):
        response = self.client.post(self.get_url_for_add(domain), {
            'new_account_email': push.new_account_email
        })
        return PushResource(**response['data'])
