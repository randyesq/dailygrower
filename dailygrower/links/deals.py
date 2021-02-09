# Objects used in the Daily Grower Site
from datetime import datetime
import os
from urllib.parse import urlparse, parse_qsl

from marshmallow import Schema, fields, post_load, pre_load
import requests

class DealsLink(object):
    """ Object representation of a Link entry """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Additional massaging
        self.tags = self.tags or []

    def __repr__(self):
        return "<DealsLink(title={self.title!r})>".format(self=self)


class DealsLinkSchema(Schema):
    """ Schema for a DealsLink """
    id = fields.Str(required=True)
    url = fields.Url(required=True)
    type = fields.Str(required=True)
    tags = fields.List(fields.Str(), missing=None)
    title = fields.Str(required=True)
    blurb = fields.Str(required=True)
    hidden = fields.Boolean(default=False, missing=None)
    available_date = fields.Date(missing=None)
    expiration_date = fields.Date(missing=None)
    image_url = fields.Url(missing=None)
    created_date = fields.DateTime(required=True)

    # class Meta:
    #     datetimeformat = '%Y-%m-%dT%H:%M:%S.000Z'

    @pre_load
    def unwrap_airtable_data_structure(self, raw_data, **kwargs):
        """ Translate an Airtable entry to a deserialized representation """
        data =  {
            'id': raw_data['id'],
            'type': raw_data['fields']['Type'],
            'url': raw_data['fields']['Link'],
            'title': raw_data['fields']['Title'],
            'blurb': raw_data['fields']['Blurb'],
            'created_date': raw_data['createdTime']
        }
        data['image_url'] = raw_data['fields'].get('Image URL', None)
        data['tags'] = raw_data['fields'].get('Tags', None)
        data['available_date'] = raw_data['fields'].get('Available Date', None)
        data['hidden'] = raw_data['fields'].get('Hidden', None)
        data['expiration_date'] = raw_data['fields'].get('Expiration Date', None)
        
        return data

    @post_load
    def make_link(self, data, **kwargs):
        return DealsLink(**data)
