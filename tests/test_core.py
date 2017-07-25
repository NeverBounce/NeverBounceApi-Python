"""
Tests the core functionality of the NeverBounce API SDK
"""
from requests import Session

import neverbounce_sdk
from neverbounce_sdk import NeverBounceAPIClient, StaticTokenAuth


def test_client_function():
    """neverbounce_sdk.client() should return a NeverBounceAPIClient()"""
    client = neverbounce_sdk.client()
    assert isinstance(client, NeverBounceAPIClient)


def test_default_client_auth_is_None():
    """A newly created client must be configured with auth"""
    client = neverbounce_sdk.client()
    assert client.auth is None


def test_setting_auth_with_string():
    """You may pass a string token directly to the NeverBounceAPIClient.auth
    property"""
    client = neverbounce_sdk.client()
    # sets the StaticTokenAuth and auth.token
    client.auth = 'this is a string!'
    assert client.auth is not None
    assert isinstance(client.auth, StaticTokenAuth)
    assert client.auth.token == 'this is a string!'


def test_setting_auth_with_StaticTokenAuth():
    """You may instantiate and pass a StaticTokenAuth object directly to the
    NeverBounceAPIClient.auth property"""
    client = neverbounce_sdk.client()
    client.auth = StaticTokenAuth('secret token')
    assert client.auth is not None
    assert isinstance(client.auth, StaticTokenAuth)
    assert client.auth.token == 'secret token'


def test_clearing_client_auth():
    """You may clear the NeverBounceAPIClient.auth propery by setting it to
    None or the ``del`` statement; they are equivalent"""
    client = neverbounce_sdk.client()
    # by directly setting the property to None
    client.auth = 'something'
    assert client.auth is not None
    client.auth = None
    assert client.auth is None
    # by "deleting" the property
    client.auth = 'something'
    assert client.auth is not None
    del client.auth
    assert client.auth is None


def test_default_client_session_is_none():
    """A newly created client has no default session"""
    client = neverbounce_sdk.client()
    assert client.session is None


def test_client_as_context_manager_has_default_requests_session():
    """When used as context manager, default client uses requests.Session"""
    with neverbounce_sdk.client() as client:
        assert client.session is not None
        assert isinstance(client.session, Session)


def test_setting_custom_session_recognized_in_context_manager():
    """When used as a context manager, a client should not override a custom
    session with the default requests one"""
    custom_session = Session()
    with neverbounce_sdk.client(session=custom_session) as client:
        assert client.session is custom_session
    # session is cleared upon exiting a context
    assert client.session is None


def test_client_auth_fallback_with_custom_session_present():
    """The NeverBounceAPIClient will fall back to using a session auth if a
    session is present but no auth"""
    custom_session = Session()
    custom_session.auth = StaticTokenAuth('secret token!')
    client = neverbounce_sdk.client(session=custom_session)
    # is: should be the same object
    assert client.session is custom_session
    assert client.auth is custom_session.auth

    custom_auth = StaticTokenAuth('different token!')
    client = neverbounce_sdk.client(session=custom_session, auth=custom_auth)
    assert client.session is custom_session
    assert client.auth is custom_auth
