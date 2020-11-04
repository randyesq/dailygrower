from datetime import datetime

def weight_links(links):
    """ Weight links in priority order based on link factors """
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
