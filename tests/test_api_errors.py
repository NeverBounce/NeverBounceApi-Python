"""
Tests the client's API Error handling
"""
import pytest
import responses

import neverbounce_sdk
from neverbounce_sdk import (urlfor,
                             NeverBounceAPIException)
from neverbounce_sdk.exceptions import _status_to_exception


@pytest.mark.parametrize('exc', list(_status_to_exception))
@responses.activate
def test_account_info(exc):
    # this is the exepcted response: we've picked a random simple API target
    # just so we can mock out some exceptions and see how the client handles
    # them
    responses.add(responses.GET,
                  urlfor('account', 'info'),
                  status=200,
                  json={'status': exc, 'message': 'the-message'})

    with pytest.raises(_status_to_exception[exc]) as raised_exc:
        neverbounce_sdk.client().account_info()

        if exc == 'auth_failure':
            assert 'NeverBounceAPIClient.auth is not set' in raised_exc.message
        else:
            assert 'the-message' in raised_exc.message


@responses.activate
def test_weird_response_no_status_raises():
    responses.add(responses.GET,
                  urlfor('account', 'info'),
                  status=200,
                  # empty dict; client should complain that there's no 'status'
                  # key
                  json={'message': None})

    with pytest.raises(NeverBounceAPIException):
        neverbounce_sdk.client().account_info()
