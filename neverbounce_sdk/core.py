"""
Core API support methods
"""
import requests

from .auth import StaticTokenAuth
from .exceptions import _status_to_exception, NeverBounceAPIException
from .utils import urlfor


class APICore(object):
    """
    Core helpers for authenticating and interacting with the Neverbounce API
    """

    def __init__(self, auth=None, session=None):
        self.auth = auth
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
        # self.session.auth if self._auth is not set and self.session is
        if not kwargs.get('auth'):
            kwargs.update({'auth': self.auth})
        if self.session:
            return self.session.request(method, url, *args, **kwargs)
        return requests.request(method, url, *args, **kwargs)

    def _check_response(self, resp):
        """Checks a response for errors and throws if they any present"""
        # first check that there were no errors on the wire
        resp.raise_for_status()
        data = resp.json()

        # now make sure we have a sensible response
        try:
            api_status = data['status']
        except KeyError:
            # no status field in the API's return object
            # complain about it cause that's weird
            raise NeverBounceAPIException(resp.json())

        # if everything is good, we're done
        if api_status == 'success':
            return resp
        # if not, construct and raise the appropriate exception
        try:
            exc = _status_to_exception[api_status]
        except KeyError:
            # this is an uknown failure from upstream; letting the KeyError
            # propgate would be weird to the user: use a generic error
            exc = NeverBounceAPIException

        message = data.get('message')
        execution_time=data.get('execution_time')

        # if the problem is with authentication, rewrite the error message to
        # make more sense in the current context
        if api_status == 'auth_failure' and not self.auth:
            message = 'NeverBounceAPIClient.auth is not set'

        raise exc(message, execution_time)

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
