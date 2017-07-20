import requests
from .auth import StaticTokenAuth

__all__ = [
    'client',
    'NeverBounceApiClient'
]

API_ROOT = 'https://api.neverbounce.com'
API_VERSION = 'v4'


def urlfor(*parts):
    """Returns the API endpoint base url (i.e. does not handle URL params)"""
    endpoint = '/'.join(parts)
    return '{}/{}/{}'.format(API_ROOT, API_VERSION, endpoint)


def client(*args, **kwargs):
    """ Factory function (alias) for NeverBounceApiClient objects """
    return NeverBounceApiClient(*args, **kwargs)


class NeverBounceApiClient(object):
    """
    An API interface object for communicating with NeverBounce's API.
    """

    def __init__(self, auth=None, session=None):
        self._auth = auth
        self.session = session

    @property
    def auth(self):
        """
        If self.session is set and self.auth is not, falls back to
        ``self.session.auth``.
        """
        if self.session and not self._auth:
            return self.session.auth
        return self._auth

    @auth.setter
    def auth(self, val):
        if val is None:
            self._auth = None
        elif isinstance(val, StaticTokenAuth):
            self._auth = val
        else:
            self._auth = StaticTokenAuth(val)

    @auth.deleter
    def auth(self):
        self._auth = None

    def _make_request(self, method, url, *args, **kwargs):
        """
        Looks for an underlying Session and uses that if available, else
        defaults to the main requests interface
        """
        # no try/except; any errors that occur down here need to propogate
        # prefer an ``auth`` from invoker, and remember self.auth falls back to
        # self.session.auth is self._auth is not set and self.session is
        if not kwargs.get('auth'):
            kwargs.update({'auth': self.auth})
        if self.session:
            return self.session.request(method, url, *args, **kwargs)
        return requests.request(method, url, *args, **kwargs)

    def __enter__(self):
        """
        When entering a context, if no session is set, use
        requests.session() as default.  Return self as the context manager
        """
        if self.session is None:
            self.session = requests.session()
        return self

    def __exit__(self, *args):
        """When exiting a context, close and clear the session"""
        self.session.close()
        self.session = None

    ######## API Methods ######################################################

    @property
    def account_info(self):
        if not hasattr(self, '_account_info'):
            endpoint = urlfor('account', 'info')
            resp = self._make_request('GET', endpoint)
            #self.check(resp)
            self._account_info = resp.json()
        return self._account_info

    @account_info.deleter
    def account_info(self):
        del self._account_info
