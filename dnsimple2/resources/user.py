from dateutil.parser import parse

from dnsimple2.resources import BaseResource


class UserResource(BaseResource):
    fields = ('id', 'email', 'created_at', 'updated_at',)

    def __init__(self, data):
        self.id = data.get('id')
        self.email = data.get('email')
        self.created_at = parse(data.get('created_at'))
        self.updated_at = parse(data.get('updated_at'))
