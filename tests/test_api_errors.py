"""
Tests the client's API Error handling
"""
import pytest
import responses

import neverbounce_sdk
from neverbounce_sdk import (urlforversion,
                             GeneralException)
from neverbounce_sdk.exceptions import _status_to_exception


@pytest.mark.parametrize('err', list(_status_to_exception))
@responses.activate
def test_account_info(err):
    # this is the exepcted response: we've picked a random simple API target
    # just so we can mock out some exceptions and see how the client handles
    # them
    responses.add(responses.GET,
                  urlforversion('v4.2', 'account', 'info'),
                  status=200,
                  json={'status': err, 'message': 'the-message'})

    with pytest.raises(_status_to_exception[err]) as exc:
        neverbounce_sdk.client().account_info()

    if err == 'auth_failure':
        assert 'We were unable to authenticate your request'\
               in str(exc.value)
    else:
        assert 'We were unable to complete your request.' in str(exc.value)
        assert err in str(exc.value)


@responses.activate
def test_non_json_response():
    responses.add(responses.GET,
                  urlforversion('v4.2', 'account', 'info'),
                  status=200,
                  # empty dict; client should complain that there's no 'status'
                  # key
                  body='Not Json')

    with pytest.raises(GeneralException) as exc:
        neverbounce_sdk.client().account_info()
    assert ('The response from NeverBounce was unable '
            + 'to be parsed as json. Try the request '
            + 'again, if this error persists'
            + ' let us know at support@neverbounce.com.'
            + '\\n\\n(Internal error)') in str(exc.value)


@responses.activate
def test_weird_response_no_status_raises():
    responses.add(responses.GET,
                  urlforversion('v4.2', 'account', 'info'),
                  status=200,
                  # empty dict; client should complain that there's no 'status'
                  # key
                  json={'message': 'Something went wrong'})

    with pytest.raises(GeneralException) as exc:
        neverbounce_sdk.client().account_info()
    assert ('The response from server is incomplete. '
            + 'Either a status code was not included '
            + 'or the an error was returned without an '
            + 'error message. Try the request again, '
            + 'if this error persists let us know at '
            + 'support@neverbounce.com.'
            + '\\n\\n(Internal error [status 200: '
            + '{"message": "Something went wrong"}])') in str(exc.value)
