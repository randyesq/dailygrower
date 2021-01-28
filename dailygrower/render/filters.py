# Custom filters for Daily Grower Templates
from urllib.parse import urlparse

import pytz


def approval_day(link, tz):
    """
    Get the day of the week (Monday, Tuesday) etc when the link was approved
    """
    LOCAL_TZ = pytz.timezone(tz)
    local_date = link.approval_date.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)
    return local_date.strftime('%A')


def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'

    https://stackoverflow.com/a/50992575/576333
    '''
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix