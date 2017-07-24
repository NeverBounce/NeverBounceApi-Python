"""
NeverBounce API Authentication
"""
from requests.auth import AuthBase

__all__ = ['StaticTokenAuth']


class StaticTokenAuth(AuthBase):
    """Uses a static token to authenticate with NeverBounce's API v4

    Args:
        token (str): A static API token for authentication
    """

    def __init__(self, token):
        self.token = token
        self.token_d = dict(key=token)

    def __call__(self, request):
        # Apparently this will work no matter what HTTP method is used, so...
        # this is simplest, just do this.  NOTE: at this point in time, if the
        # request is a POST/PATCH/PUT, the body is already encoded and there is
        # no non-ugly way to just attach the token to it
        request.prepare_url(request.url, self.token_d)
        return request
