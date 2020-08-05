# -*- coding: utf-8 -*-
__author__ = "NeverBounce Team"
__email__ = 'support@neverbounce.com'
__version__ = '4.3.0'

from .auth import *         # noqa: F403
from .exceptions import *   # noqa: F403
from .utils import *        # noqa: F403

from .account import AccountMixin
from .bulk import JobRunnerMixin
from .core import APICore
from .poe import POEMixin
from .single import SingleMixin

__all__ = (auth.__all__ +           # noqa: F405
           exceptions.__all__ +     # noqa: F405
           utils.__all__ +          # noqa: F405
           ['NeverBounceAPIClient', 'client'])


class NeverBounceAPIClient(AccountMixin,
                           SingleMixin,
                           JobRunnerMixin,
                           POEMixin,
                           APICore):
    pass


def client(*args, **kwargs):
    """ Factory function (alias) for NeverBounceAPIClient objects """
    return NeverBounceAPIClient(*args, **kwargs)
