"""
Tests the POE endpoints
"""
import responses

import neverbounce_sdk
from neverbounce_sdk import urlforversion


@responses.activate
def test_poe_confirm():
    # this is the exepcted response
    responses.add(responses.GET,
                  urlforversion('v4.2', 'poe', 'confirm'),
                  status=200,
                  json={'status': 'success'})

    with neverbounce_sdk.client(api_key='static key') as client:
        info = client.poe_confirm(
            email='support@neverbounce.com',
            transaction_id='NBPOE-TXN-5942940c09669',
            confirmation_token='e3173fdbbdce6bad26522dae792911f2',
            result='valid')

    assert info == {'status': 'success'}
    assert len(responses.calls) == 1
    url = responses.calls[0].request.url
    for urlchunk in ('https://api.neverbounce.com/v4.2/poe/confirm',
                     'email=support%40neverbounce.com',
                     'transaction_id=NBPOE-TXN-5942940c09669',
                     'confirmation_token=e3173fdbbdce6bad26522dae792911f2',
                     'result=valid'):
        assert urlchunk in url
