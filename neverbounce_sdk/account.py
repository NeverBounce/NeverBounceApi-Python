"""
API support for endpoints located at API_ROOT/account
"""
from .utils import urlfor


class AccountMixin(object):
    __doc__ = __doc__

    def account_info(self):
        """Provides information about the authenticated caller's account.

        Returns:
            A ``dict``

        See also:
            https://developers.neverbounce.com/v4.0/reference#account-info
        """
        endpoint = urlfor('account', 'info', api_version=self.api_version)
        resp = self._make_request('GET', endpoint)
        self._check_response(resp)
        return resp.json()
