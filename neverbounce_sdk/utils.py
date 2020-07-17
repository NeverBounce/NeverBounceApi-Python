"""
Utility functions and constants used in the codebase
"""

__all__ = [
    'API_ROOT',
    'API_VERSION',
    'urlfor',
    'urlforversion'
]

API_ROOT = 'https://api.neverbounce.com'
API_VERSION = 'v4.2'


def urlfor(*parts):
    """Returns the API endpoint base url (i.e. does not handle URL params)"""
    return urlforversion(API_VERSION, *parts)


def urlforversion(api_version, *parts):
    """Returns the API endpoint base url (i.e. does not handle URL params)"""
    endpoint = '/'.join(parts)
    return '{}/{}/{}'.format(API_ROOT, api_version, endpoint)
