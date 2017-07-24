# -*- coding: utf-8 -*-

__author__ = "NeverBounce Team"
__email__ = 'support@neverbounce.com'
__version__ = '0.1.0.dev1'


from .auth import *
from .exceptions import *
from .utils import *

from .account import AccountMixin
from .bulk import JobRunnerMixin
from .core import APICore
from .single import SingleMixin


__all__ = (auth.__all__ +
           exceptions.__all__ +
           utils.__all__ +
           ['NeverBounceAPIClient', 'client'])


class NeverBounceAPIClient(AccountMixin, SingleMixin, JobRunnerMixin, APICore):
    pass


def client(*args, **kwargs):
    """ Factory function (alias) for NeverBounceAPIClient objects """
    return NeverBounceAPIClient(*args, **kwargs)
