from dnsimple2 import resources


class CertificateResource(resources.BaseResource):
    def __init__(self, **kwargs):
        super(CertificateResource, self).__init__(**kwargs)

        self.id = kwargs.get('id')
        self.domain_id = kwargs.get('domain_id')
        self.name = kwargs.get('name')
        self.common_name = kwargs.get('common_name')
        self.years = kwargs.get('years')
        self.csr = kwargs.get('csr')
        self.state = kwargs.get('state')
        self.authority_identifier = kwargs.get('authority_identifier')
        self.created_at = self.parse_datetime(kwargs.get('created_at'))
        self.updated_at = self.parse_datetime(kwargs.get('updated_at'))
        self.expires_on = self.parse_date(kwargs.get('expires_on'))
