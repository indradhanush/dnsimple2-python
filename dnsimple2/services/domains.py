from dnsimple2.resources import (
    CollaboratorResource,
    DomainResource,
    EmailForwardResource
)
from dnsimple2.services import BaseService


class DomainService(BaseService):
    def __init__(self, client):
        super(DomainService, self).__init__(client, '{account_id}/domains')
        self.collaborators = CollaboratorService(self)
        self.email_forwards = EmailForwardService(self)

    def get_url(self, account_id, domain=None):
        url = self.url.format(account_id=account_id)
        if domain is not None:
            return url + '/{domain}'.format(domain=domain)

        return url

    def list(self, account_id, **kwargs):
        response = self.client.get(self.get_url(account_id), **kwargs)
        return [DomainResource(item) for item in response['data']]

    def get(self, account_id, domain, **kwargs):
        response = self.client.get(self.get_url(account_id, domain), **kwargs)
        return DomainResource(response['data'])

    def create(self, account_id, data):
        response = self.client.post(self.get_url(account_id), data)
        return DomainResource(response['data'])

    def delete(self, account_id, domain):
        self.client.delete(self.get_url(account_id, domain))

    def reset_token(self, account_id, domain):
        url = self.get_url(account_id, domain) + "/token"
        response = self.client.post(url)
        return DomainResource(response['data'])


class CollaboratorService(BaseService):
    def __init__(self, domains):
        super(CollaboratorService, self).__init__(
            domains.client,
            '{account_id}/domains/{domain_id}/collaborators'
        )
        self.domains = domains

    def get_url(self, domain, collaborator=None):
        url = self.url.format(account_id=domain.account_id, domain_id=domain.id)
        if collaborator is not None:
            return url + '/{collaborator_id}'.format(collaborator_id=collaborator.id)

        return url

    def list(self, domain):
        response = self.client.get(self.get_url(domain))
        return [CollaboratorResource(item) for item in response['data']]

    def add(self, domain, collaborator):
        response = self.client.post(self.get_url(domain), {
            'email': collaborator.user_email
        })
        return CollaboratorResource(response['data'])

    def delete(self, domain, collaborator):
        self.client.delete(self.get_url(domain, collaborator))


class EmailForwardService(BaseService):
    def __init__(self, domain_service):
        super(EmailForwardService, self).__init__(
            client=domain_service.client,
            endpoint='{account_id}/domains/{domain_id}/email_forwards'
        )

    def get_url(self, domain, email_forward=None):
        url = self.url.format(account_id=domain.account_id, domain_id=domain.id)
        if email_forward is not None:
            return url + '/{email_forward_id}'.format(email_forward_id=email_forward.id)

        return url

    def list(self, domain):
        response = self.client.get(self.get_url(domain))
        return [EmailForwardResource(item) for item in response['data']]

    def get(self, domain, email_forward):
        response = self.client.get(self.get_url(domain, email_forward))
        return EmailForwardResource(response['data'])

    def create(self, domain, email_forward):
        response = self.client.post(self.get_url(domain), {
            'from': email_forward.from_email,
            'to': email_forward.to
        })
        return EmailForwardResource(response['data'])

    def delete(self, domain, email_forward):
        self.client.delete(self.get_url(domain, email_forward))
