# Airtable module
import datetime
import posixpath
from urllib.parse import urljoin

import requests


AIRTABLE_API_BASE_URL = "https://api.airtable.com"
AIRTABLE_API_VERSION = "v0"


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


def fetch_links(base_id="app79OUH4JFgpGic3", view="Live", table="Content", api_key="keyYyJtgn4NboX8b7"):
    """ Fetch the links from the `view` view and the `table` table. """
    url_path = posixpath.join(AIRTABLE_API_VERSION, base_id, table)
    url = urljoin(AIRTABLE_API_BASE_URL, url_path)
    r = requests.get(url, params={'view': view, 'userLocale': 'America/Chicago'}, auth=BearerAuth(api_key))
    records = r.json()['records']
    for rec in records:
        if 'Approval Date' in rec['fields']:
            rec['fields']['Approval Date'] = datetime.datetime.strptime(rec['fields']['Approval Date'], '%Y-%m-%dT%H:%M:%S.000Z')
    return records


def get_link_tags(links):
    """ From the list of links, get the tags """
    tags = set()
    for link in links:
        tags.update(link['fields']['Link Tags'])
    return tags
