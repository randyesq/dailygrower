# Objects used in the Daily Grower Site
from datetime import datetime
import os
from urllib.parse import urlparse, parse_qsl

from marshmallow import Schema, fields, post_load, pre_load
import requests


YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


class Link(object):
    """ Object representation of a Link entry """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Additional massaging
        self.tags = self.tags or []

        # Additional fields besides the schema-defined fields
        self.netloc = urlparse(self.url).netloc

        # Additional processing of schema-defined fields
        # If this is a YouTube link and there is no other image
        # set for it, get the YouTube thumbnail
        if self.is_youtube_link():
            if self.image_url is None:
                self.image_url = self.fetch_youtube_thumbnail()

            # For YouTube Links, set the netloc to the channel name instead of
            # the YouTube domain name
            channel = self.fetch_youtube_channel_name()
            self.netloc = "YouTube: {}".format(channel)

    def __repr__(self):
        return "<Link(headline={self.headline!r})>".format(self=self)

    def is_youtube_link(self):
        return any([nl in self.netloc for nl in ['youtube.com', 'youtu.be'] ])

    def fetch_youtube_thumbnail(self):
        """
        Fetch a youtube thumbmail image
        # https://stackoverflow.com/questions/2068344/how-do-i-get-a-youtube-video-thumbnail-from-the-youtube-api
        """
        vid = dict(parse_qsl(urlparse(self.url).query))['v']
        return 'https://i.ytimg.com/vi_webp/{}/maxresdefault.webp'.format(vid)

    def fetch_youtube_channel_name(self):
        """
        Use the YouTube Data API to get the name of the channel based on the
        video id
        """
        vid = dict(parse_qsl(urlparse(self.url).query))['v']
        resp = requests.get(
            'https://youtube.googleapis.com/youtube/v3/videos',
            headers={"Content-type": "application/json"},
            params={
                "key": YOUTUBE_API_KEY,
                "part": "snippet",
                "id": vid
            }
        )
        resp.raise_for_status()
        return resp.json()['items'][0]['snippet']['channelTitle']


class LinkSchema(Schema):
    """ Schema for a Link """
    id = fields.Str(required=True)
    url = fields.Url(required=True)
    tags = fields.List(fields.Str(), missing=None)
    headline = fields.Str(required=True)
    blurb = fields.Str(required=True)
    featured = fields.Boolean(default=False, missing=None)
    approved = fields.Boolean(default=False, missing=None)
    approval_date = fields.DateTime(missing=None)
    archived = fields.Boolean(default=False, missing=None)
    archive_date = fields.DateTime(missing=None)
    image_url = fields.Url(missing=None)
    image_alt = fields.Str(missing=None)
    created_date = fields.DateTime(required=True)

    class Meta:
        datetimeformat = '%Y-%m-%dT%H:%M:%S.000Z'

    @pre_load
    def unwrap_airtable_data_structure(self, raw_data, **kwargs):
        """ Translate an Airtable entry to a deserialized representation """
        data =  {
            'id': raw_data['id'],
            'url': raw_data['fields']['Link'],
            'headline': raw_data['fields']['Headline'],
            'blurb': raw_data['fields']['Blurb'],
            'created_date': raw_data['createdTime']
        }
        data['featured'] = raw_data['fields'].get('Featured', None)
        data['tags'] = raw_data['fields'].get('Link Tags', None)
        data['approved'] = raw_data['fields'].get('Approved', None)
        data['approval_date'] =raw_data['fields'].get('Approval Date', None)
        data['archived'] = raw_data['fields'].get('Archived', None)
        data['archive_date'] =raw_data['fields'].get('Archive Date', None)
        data['image_url'] = raw_data['fields'].get('Image URL', None)
        data['image_alt'] = raw_data['fields'].get('Image Alt', None)
        return data

    @post_load
    def make_link(self, data, **kwargs):
        return Link(**data)
