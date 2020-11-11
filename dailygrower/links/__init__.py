from datetime import datetime
from urllib.parse import urlparse

def weight_links(links):
    """
    Weight links in priority order based on link factors. Add the value to a
    `score` member on the link dictionary. Return the modified `links` list
    sorted by `score` in descending order.
    """
    now = datetime.utcnow()
    for link in links:
        raw_weight = link['fields']['Weight']
        expiration = datetime.strptime(
            link['fields']['Expiration Date'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        ttl = (expiration - now).total_seconds()
        duration = link['fields']['Duration'] * 24 * 60 * 60
        ttl_factor = ttl / duration
        weight_factor = (raw_weight + 100) / 2 
        link['score'] = ttl_factor*weight_factor

    return sorted(links, key=lambda l: l['score'], reverse=True)


def parse_netloc(links):
    """
    Parse the net location of a list of links. Add the value to a 'netloc'
    member on the link dictionary
    """
    for link in links:
        link['netloc'] = urlparse(link['fields']['Link']).netloc
    return links
