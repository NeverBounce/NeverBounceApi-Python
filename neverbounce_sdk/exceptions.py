"""
NeverBounce API exceptions and warnings
"""

__all__ = ['GeneralException',
           'AuthFailure',
           'ThrottleTriggered',
           'BadReferrer']


class GeneralException(Exception):
    """
    A non recoverable API error occurred check the message for details
    """

    def __init__(self, message, execution_time=None):
        self.execution_time = execution_time
        self.message = message
        super(GeneralException, self).__init__(message, execution_time)


class AuthFailure(GeneralException):
    """
    The API credentials used are bad, have you reset them recently?
    """


class ThrottleTriggered(GeneralException):
    """
    Too many requests in a short amount of time, try again shortly or adjust
    your rate limit settings for this application in the dashboard
    """


class BadReferrer(GeneralException):
    """
    The script is being used from an unauthorized source, you may need to
    adjust your app's settings to allow it to be used from here
    """


_status_to_exception = {
    'general_failure': GeneralException,
    'auth_failure': AuthFailure,
    'throttle_triggered': ThrottleTriggered,
    'bad_referrer': BadReferrer
}
