# Airtable module
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
    return r.json()