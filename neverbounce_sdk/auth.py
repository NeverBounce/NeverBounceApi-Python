"""
NeverBounce API Authentication
"""
from requests.auth import AuthBase
from .exceptions import UnsupportedMethod

__all__ = ['StaticTokenAuth']


class StaticTokenAuth(AuthBase):
    """Uses a static token to authenticate with NeverBounce's API v4"""

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        if request.method == 'GET':
            request.params.update({'key': self.token})
        elif request.method == 'POST':
            request.data.update({'key': self.token})
        else:
            raise UnsupportedMethod('HTTP verb %s is unsupported' %
                                    request.method)
