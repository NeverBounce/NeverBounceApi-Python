"""
Tests the Single endpoints
"""
import pytest
import responses

import neverbounce_sdk
from neverbounce_sdk import urlfor


@responses.activate
def test_single_check():
    # this is the exepcted response
    responses.add(responses.GET,
                  urlfor('single', 'check'),
                  status=200,
                  json={'status': 'success'})

    with neverbounce_sdk.client(auth='static key') as client:
        info = client.verify('test@example.com', credits_info=True)

    assert info == {'status': 'success'}
    assert len(responses.calls) == 1
    url = responses.calls[0].request.url
    for urlchunk in ('https://api.neverbounce.com/v4/single/check',
                     'email=test%40example.com',
                     'address_info=0',
                     'credits_info=1',
                     'max_execution_time=30',
                     'key=static+key'):
        assert urlchunk in url
