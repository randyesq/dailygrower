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


class LinksAirtableView(object):
    """ A class for interacting with AirTable Views """

    def __init__(self, base_id, table, view, api_key):
        self.base_id = base_id
        self.table = table
        self.view = view
        self.auth = BearerAuth(api_key)

    def __repr__(self):
        return 'Links-type Base: table={}, view={}, id={}'.format(self.table, self.view, self.base_id)

    def _get_table_url(self):
        """ Get the url for a table in a base """
        url_path = posixpath.join(AIRTABLE_API_VERSION, self.base_id, self.table)
        return urljoin(AIRTABLE_API_BASE_URL, url_path)

    def get_view_records(self, locale="America/Chicago"):
        """ Get the records in a view of a table """
        url = self._get_table_url()
        r = requests.get(
            url,
            params={'view': self.view, 'userLocale': 'America/Chicago'},
            auth=self.auth
        )
        r.raise_for_status()
        records = r.json()['records']
        return self.sanitize_records(list(records))

    def approve_record(self, record):
        """ Approve a record in the table """
        url = self._get_table_url()
        r = requests.patch(
            url,
            auth=self.auth,
            json={
                "records": [{"id": record["id"], "fields": { "Approved": True }}]
            }
        )
        r.raise_for_status()
        return self.sanitize_records([r.json()['records'][0]])

    def sanitize_records(self, records):
        """ Pythonize fields that don't convert from the JSON """
        for rec in records:
            if 'Approval Date' in rec['fields']:
                rec['fields']['Approval Date'] = datetime.datetime.strptime(
                    rec['fields']['Approval Date'],
                    '%Y-%m-%dT%H:%M:%S.000Z'
                )
            if 'createdTime' in rec:
                rec['createdTime'] = datetime.datetime.strptime(
                    rec['createdTime'],
                    '%Y-%m-%dT%H:%M:%S.000Z'
                )
        return records


def get_next_link(records):
    """
    Fetch the record with either the newest featured link or the oldest
    submitted link. The allows the link submitted to pull the oldest off
    the shelf to keep links from getting stale or to prioritize a featured
    link that can pop to the stop of the stack.
    """
    if not records:
        return None

    next_link = records[0]
    featured = sorted(
        [record for record in records
            if 'Featured' in record['fields'] and record['fields']['Featured']
        ],
        key=lambda x: (x['createdTime'])
    )

    # return the newest one
    if featured:
        return featured[-1]

    # Return the oldest of the links since none are featured
    pending = sorted(
        [record for record in records],
        key=lambda x: (x['createdTime'])
    )
    return pending[0]