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
    assert client.api_key is None


def test_setting_auth_with_string():
    """You may pass a string api_key directly to the NeverBounceAPIClient.api_key
    property"""
    client = neverbounce_sdk.client()
    # sets the StaticTokenAuth and auth.api_key
    client.api_key = 'this is a string!'
    assert client.api_key is not None
    assert isinstance(client.api_key, StaticTokenAuth)
    assert client.api_key.api_key == 'this is a string!'


def test_setting_auth_with_StaticTokenAuth():
    """You may instantiate and pass a StaticTokenAuth object directly to the
    NeverBounceAPIClient.api_key property"""
    client = neverbounce_sdk.client()
    client.api_key = StaticTokenAuth('secret token')
    assert client.api_key is not None
    assert isinstance(client.api_key, StaticTokenAuth)
    assert client.api_key.api_key == 'secret token'


def test_clearing_client_auth():
    """You may clear the NeverBounceAPIClient.api_key propery by setting it to
    None or the ``del`` statement; they are equivalent"""
    client = neverbounce_sdk.client()
    # by directly setting the property to None
    client.api_key = 'something'
    assert client.api_key is not None
    client.api_key = None
    assert client.api_key is None
    # by "deleting" the property
    client.api_key = 'something'
    assert client.api_key is not None
    del client.api_key
    assert client.api_key is None


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
    custom_session.api_key = StaticTokenAuth('secret token!')
    client = neverbounce_sdk.client(session=custom_session)
    # is: should be the same object
    assert client.session is custom_session
    assert client.api_key is custom_session.api_key

    custom_auth = StaticTokenAuth('different token!')
    client = neverbounce_sdk.client(session=custom_session,
                                    api_key=custom_auth)
    assert client.session is custom_session
    assert client.api_key is custom_auth


def test_default_client_timeout_is_default():
    """A newly created client must be configured with default timeout"""
    client = neverbounce_sdk.client()
    assert client.timeout == 30


def test_setting_timeout_with_None():
    """You may set timeout to None in the NeverBounceAPIClient.timeout
    property"""
    client = neverbounce_sdk.client()
    client.timeout = None
    assert client.timeout is None


def test_setting_timeout_with_integer():
    """You may set timeout to an integer in the NeverBounceAPIClient.timeout
    property"""
    client = neverbounce_sdk.client()
    client.timeout = 5
    assert client.timeout == 5


def test_default_client_api_version_is_default():
    """A newly created client must be configured with default api_version"""
    client = neverbounce_sdk.client()
    assert client.api_version == "v4.2"


def test_setting_api_version():
    """You may set API version NeverBounceAPIClient.api_version property"""
    client = neverbounce_sdk.client("api_key", None, 1, "some_version")
    assert client.api_version == "some_version"


def test_setting_api_version_by_name():
    """You may set API version NeverBounceAPIClient.api_version property"""
    client = neverbounce_sdk.client(api_version="some_other_version")
    assert client.api_version == "some_other_version"
