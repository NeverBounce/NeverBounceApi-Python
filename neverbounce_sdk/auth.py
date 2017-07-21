"""
NeverBounce API Authentication
"""
from requests.auth import AuthBase

__all__ = ['StaticTokenAuth']


class StaticTokenAuth(AuthBase):
    """Uses a static token to authenticate with NeverBounce's API v4"""

    def __init__(self, token):
        self.token = token
        self.token_d = dict(key=token)

    def __call__(self, request):
        if request.method == 'GET':
            request.prepare_url(request.url, self.token_d)
        elif request.method == 'POST':
            request.data.update(self.token_d)
        return request
