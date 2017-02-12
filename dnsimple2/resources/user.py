from dnsimple2.resources import BaseResource


class UserResource(BaseResource):
    fields = ('id', 'email', 'created_at', 'updated_at',)

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        self.created_at = self.parse_datetime(kwargs.get('created_at'))
        self.updated_at = self.parse_datetime(kwargs.get('updated_at'))
