from dnsimple2.resources import (
    AccountResource,
    BaseResource,
    UserResource
)


class WhoAmIResource(BaseResource):
    fields = ('user', 'account',)

    def __init__(self, **kwargs):
        user = kwargs.get('user') or {}
        account = kwargs.get('account') or {}

        self.user = UserResource(**user)
        self.account = AccountResource(**account)
