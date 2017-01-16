from dnsimple2.resources import (
    AccountResource,
    BaseResource,
    UserResource
)


class WhoAmIResource(BaseResource):
    fields = ('user', 'account',)

    def __init__(self, data):
        if data is None:
            return

        self.user = UserResource(data['user'])
        self.account = AccountResource(data['account'])
