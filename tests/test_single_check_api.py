"""
Tests the Single endpoints
"""
import responses

import neverbounce_sdk
from neverbounce_sdk import urlforversion, urlfor


@responses.activate
def test_single_check():
    # this is the exepcted response
    responses.add(responses.GET,
                  urlfor('single', 'check'),
                  status=200,
                  json={'status': 'success'})

    with neverbounce_sdk.client(api_key='static key') as client:
        info = client.single_check('test@example.com', credits_info=True)

    assert info == {'status': 'success'}
    assert len(responses.calls) == 1
    url = responses.calls[0].request.url
    for urlchunk in ('https://api.neverbounce.com/v4.2/single/check',
                     'email=test%40example.com',
                     'address_info=0',
                     'credits_info=1',
                     'timeout=30',
                     'key=static+key'):
        assert urlchunk in url


@responses.activate
def test_single_check_with_specific_version():
    # this is the exepcted response
    responses.add(responses.GET,
                  urlforversion('v4.2', 'single', 'check'),
                  status=200,
                  json={'status': 'success'})

    with neverbounce_sdk.client(api_key='abc', api_version="v4.2") as client:
        info = client.single_check('test@example.com', credits_info=True)

    assert info == {'status': 'success'}
    assert len(responses.calls) == 1
    url = responses.calls[0].request.url
    for urlchunk in ('https://api.neverbounce.com/v4.2/single/check',
                     'email=test%40example.com',
                     'address_info=0',
                     'credits_info=1',
                     'timeout=30',
                     'key=abc'):
        assert urlchunk in url
