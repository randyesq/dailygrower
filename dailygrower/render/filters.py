# Custom filters for Daily Grower Templates
from urllib.parse import urlparse

import pytz


def netloc(url):
    """ Parse the net location of a url """
    return urlparse(url).netloc


def approval_day(link, tz):
    """
    Get the day of the week (Monday, Tuesday) etc when the link was approved
    """
    LOCAL_TZ = pytz.timezone(tz)
    local_date = link['fields']['Approval Date'].replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)
    return local_date.strftime('%A')
