"""
NeverBounce API exceptions and warnings
"""

__all__ = ['NeverBounceAPIException',
           'UnsupportedMethod']


class NeverBounceAPIException(Exception):
    """Base class for NeverBounce API errors"""


class UnsupportedMethod(NeverBounceAPIException):
    """The API supports only GET and POST"""
