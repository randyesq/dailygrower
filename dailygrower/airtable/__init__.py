# Airtable module
import os
import datetime
import posixpath
from urllib.parse import urljoin, urlparse, parse_qsl

import requests

from dailygrower.links import LinkSchema
from dailygrower.links.deals import DealsLinkSchema


AIRTABLE_API_BASE_URL = "https://api.airtable.com"
AIRTABLE_API_VERSION = "v0"
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class AirtableView(object):
    """ A class for interacting with AirTable Views """
    schema = None

    def __init__(self, base_id, table, view, api_key=AIRTABLE_API_KEY):
        self.base_id = base_id
        self.table = table
        self.view = view
        self.auth = BearerAuth(api_key)

    def __repr__(self):
        return 'Base: table={}, view={}, id={}'.format(self.table, self.view, self.base_id)

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
        return self.schema.load(list(records), many=True)


class DealsLinkAirtableView(AirtableView):
    schema = DealsLinkSchema()


class LinksAirtableView(AirtableView):
    """ A class for interacting with AirTable Views for Links """
    schema = LinkSchema()

    def approve_records(self, records):
        """ Approve records in the table """
        url = self._get_table_url()
        patched_records = []
        for record in records:
            r = requests.patch(
                url,
                auth=self.auth,
                json={
                    "records": [{"id": record.id, "fields": { "Approved": True }}]
                }
            )
            r.raise_for_status()
            patched_records.append(r.json()['records'][0])
        return self.schema.load(list(patched_records), many=True)

    def archive_records(self, records):
        """ Archive records in the table """
        url = self._get_table_url()
        patched_records = []
        for record in records:
            r = requests.patch(
                url,
                auth=self.auth,
                json={
                    "records": [{"id": record.id, "fields": { "Archived": True }}]
                }
            )
            r.raise_for_status()
            patched_records.append(r.json()['records'][0])
        return self.schema.load(list(patched_records), many=True)


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
        [r for r in records if r.featured], key=lambda x: (x.created_date)
    )

    # Return the newest one
    if featured:
        return [featured[-1]]

    # Return the oldest of the links since none are featured
    pending = sorted(
        [record for record in records],
        key=lambda x: (x.created_date)
    )
    return [pending[0]]