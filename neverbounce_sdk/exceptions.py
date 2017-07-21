"""
NeverBounce API exceptions and warnings
"""

__all__ = ['NeverBounceAPIException',
           'UnsupportedMethod',
           'AuthFailure',
           'TemporarilyUnavailable',
           'ThrottleTriggered',
           'BadReferrer']


class NeverBounceAPIException(Exception):
    """Base class for NeverBounce API errors"""

    def __init__(self, message, execution_time=None):
        self.message = message
        self.execution_time = execution_time


class UnsupportedMethod(NeverBounceAPIException):
    """The API supports only the GET and POST HTTP verbs"""


class AuthFailure(NeverBounceAPIException):
    """The request couldn't be authenticated; check the API key and make sure
    it's being sent correctly"""


class TemporarilyUnavailable(NeverBounceAPIException):
    """An internal error has occurred; typically this indicates a service
    interruption"""


class ThrottleTriggered(NeverBounceAPIException):
    """The request was rejected due to rate limiting; try again shortly"""


class BadReferrer(NeverBounceAPIException):
    """The referrer for this request is not trusted"""


_status_to_exception = {
    'general_failure': NeverBounceAPIException,
    'auth_failure': AuthFailure,
    'temp_unavail': TemporarilyUnavailable,
    'throttle_triggered': ThrottleTriggered,
    'bad_referrer': BadReferrer
}
