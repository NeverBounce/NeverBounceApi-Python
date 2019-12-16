"""
API support for endpoints located at API_ROOT/single
"""
from .utils import urlforversion


class SingleMixin(object):
    __doc__ = __doc__

    def single_check(self, email,
                     address_info=False,
                     credits_info=False,
                     historical_data=True,
                     timeout=30):
        """Provides verification for a single email.

        Arguments:
            email (str): the email address to verify
            address_info (bool): If ``True``, return extra information about
                the address. Default is ``False``.
            credits_info (bool): If ``True``, return extra information about
                the account and how many credits remain.  Default is ``False``.
            historical_data (bool): If ``True``, return historical data.
                Default is ``True``.
            timeout (int): Set a timeout for the verification. Once this limit
                is reached the API will give up verifying the email and return
                it as an "Unknown". This is enforced by the API, NOT the local
                request library (for setting request timeouts use the
                ``timeout`` parameter on the client). Default is ``30``.

        Returns:
            A ``dict``

        See Also:
            https://developers.neverbounce.com/v4.0/reference#single-check
        """
        endpoint = urlforversion(self.api_version, 'single', 'check')
        params = dict(email=email,
                      # convert boolean flags to 0 or 1
                      address_info=int(address_info),
                      credits_info=int(credits_info),
                      timeout=timeout)
        historical_data_key = 'request_meta_data[leverage_historical_data]'
        params[historical_data_key] = int(historical_data)
        resp = self._make_request('GET', endpoint, params=params)
        self._check_response(resp)
        return resp.json()
