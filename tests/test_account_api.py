"""
Tests the Accounts endpoints
"""
import pytest
import responses

import neverbounce_sdk
from neverbounce_sdk import urlfor


@responses.activate
def test_account_info():
    client = neverbounce_sdk.client()
    client.auth = 'static key'

    # this is the exepcted response
    responses.add(responses.GET,
                  urlfor('account', 'info'),
                  status=200,
                  json={'status': 'success'})

    info = client.account_info()
    assert info == {'status': 'success'}
    assert len(responses.calls) == 1
    assert (responses.calls[0].request.url ==
            'https://api.neverbounce.com/v4/account/info?key=static+key')
