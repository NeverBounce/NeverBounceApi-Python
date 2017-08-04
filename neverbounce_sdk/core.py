"""
Core API support methods
"""
import requests

from . import __version__ as VERSION
from .auth import StaticTokenAuth
from .exceptions import _status_to_exception, NeverBounceAPIException


class APICore(object):
    """
    Core helpers for authenticating and interacting with the Neverbounce API
    """

    def __init__(self, api_key=None, session=None):
        self.api_key = api_key
        self.session = session

    @property
    def api_key(self):
        """
        If self.session is set and self.auth is not, falls back to
        ``self.session.auth``.
        """
        if self.session and not self._api_key:
            return self.session.api_key
        return self._api_key

    @api_key.setter
    def api_key(self, val):
        if val is None:
            self._api_key = None
        elif isinstance(val, StaticTokenAuth):
            self._api_key = val
        else:
            self._api_key = StaticTokenAuth(val)

    @api_key.deleter
    def api_key(self):
        self._api_key = None

    def _make_request(self, method, url, *args, **kwargs):
        """
        Looks for an underlying Session and uses that if available, else
        defaults to the main requests interface
        """
        # no try/except; any errors that occur down here need to propogate
        # prefer an ``auth`` from invoker, and remember self.auth falls back to
        # self.session.auth if self._auth is not set and self.session is
        headers = kwargs.pop('headers', {})
        user_agent = 'NeverBounceAPI-Python/{}'.format(VERSION)
        headers.update({'User-Agent': user_agent})
        kwargs['headers'] = headers

        if not kwargs.get('auth'):
            kwargs.update({'auth': self.api_key})
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
        execution_time = data.get('execution_time')

        # if the problem is with authentication, rewrite the error message to
        # make more sense in the current context
        if api_status == 'auth_failure' and not self.api_key:
            message = 'NeverBounceAPIClient.api_key is not set'

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
