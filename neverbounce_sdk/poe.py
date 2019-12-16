"""
API support for endpoints located at API_ROOT/poe
"""
from .utils import urlforversion


class POEMixin(object):
    __doc__ = __doc__

    def poe_confirm(self, email, transaction_id, confirmation_token, result):
        """Allows confirmation of client side verification (javscript widget)

        Arguments:
            email (str): the email address that was verified
            transaction_id: the transaction_id provided by the javascript
                widget
            confirmation_token: the confirmation_token provided by the
                javascript widget
            result: the verification result provided by the javascript widget

        Returns:
            A ``dict``

        See Also:
            https://developers.neverbounce.com/v4.0/reference#widget-poe-confirm
        """
        endpoint = urlforversion(self.api_version, 'poe', 'confirm')
        params = dict(email=email,
                      transaction_id=transaction_id,
                      confirmation_token=confirmation_token,
                      result=result)
        resp = self._make_request('GET', endpoint, params=params)
        self._check_response(resp)
        return resp.json()
