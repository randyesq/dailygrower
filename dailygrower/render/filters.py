# Custom filters for Daily Grower Templates
from urllib.parse import urlparse

import pytz
LOCAL_TZ = pytz.timezone('America/Chicago')

def netloc(url):
    """ Parse the net location of a url """
    return urlparse(url).netloc


def approval_day(link):
    """
    Get the day of the week (Monday, Tuesday) etc when the link was approved
    """
    local_date = link['fields']['Approval Date'].replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)
    return local_date.strftime('%A')
