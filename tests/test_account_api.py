"""
Tests the Accounts endpoints
"""
import responses

import neverbounce_sdk
from neverbounce_sdk import urlforversion


@responses.activate
def test_account_info():
    client = neverbounce_sdk.client()
    client.api_key = 'static key'

    # this is the exepcted response
    responses.add(responses.GET,
                  urlforversion('v4.2', 'account', 'info'),
                  status=200,
                  json={'status': 'success'})

    info = client.account_info()
    assert info == {'status': 'success'}
    assert len(responses.calls) == 1
    assert (responses.calls[0].request.url ==
            'https://api.neverbounce.com/v4.2/account/info?key=static+key')
