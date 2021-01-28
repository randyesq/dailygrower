# dailygrower.render package
"""
Render the site templates given the gathered information from
other sources (dbs, config, etc).
"""
import datetime
import math
from pathlib import Path
import os

from jinja2 import Environment, FileSystemLoader
import pytz

from dailygrower.render.filters import approval_day, make_ordinal

# Template rendering output directory
OUTPUT_DIR = Path(os.environ.get(
    'OUTPUT_DIR', Path(__file__).parent.parent.parent.joinpath('output'))
)

# Jinja Environment
ENV = Environment(
    loader=FileSystemLoader(
        Path(__file__).parent.parent.parent.joinpath('templates')
    ),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)
ENV.filters['approval_day'] = approval_day
ENV.filters['make_ordinal'] = make_ordinal

# Static templates that don't need content from DBs
STATIC_TEMPLATES = [
    "about.html.j2",
    "contribute.html.j2",
    "contrib-thanks.html.j2",
    "subscribe.html.j2",
    "subscribe-thanks.html.j2"
]

# Templates containing link content
LINK_CONTENT_TEMPLATES = [ "index.html.j2", ]
LINK_ARCHIVE_CONTENT_TEMPLATES = [ "archive.html.j2", ]

# All templates
ALL_TEMPLATES = STATIC_TEMPLATES + \
    LINK_CONTENT_TEMPLATES + LINK_ARCHIVE_CONTENT_TEMPLATES


def render_full_site(config, link_content=None):
    """ Render all of the content templates and static templates """
    render_static(config)
    if link_content:
        render_link_content(config, link_content)


def render_static(config):
    """ Render all of the static templates """
    data = construct_global_data(config)
    for template in STATIC_TEMPLATES:
        render_and_write(template, ENV.get_template(template, globals=data))


def render_and_write(template_name, template):
    """ Render the jinja template and write it to the output location """
    # Write the template file (removing the .j2 extension) to the output_dir
    with open(str(OUTPUT_DIR/Path(template_name).stem), 'w') as template_output_file:
        template_output_file.write(template.render())


def render_link_content(config, link_content):
    """ Render templates that depend on link content """
    # Current links
    data = construct_global_data(config)
    data['links'] = link_content['current'].get_view_records()
    data['links'].sort(key=lambda x: x.approval_date, reverse=True)

    for template in LINK_CONTENT_TEMPLATES:
        render_and_write(template, ENV.get_template(template, globals=data))

    # Archived links
    data['links'] = link_content['archived'].get_view_records()
    data['links'].sort(key=lambda x: x.approval_date, reverse=True)
    data['link_archive_page'] = True
    data['num_link_pages'] = math.ceil(len(data['links']) / 5)  # Five archive links per page
    for template in LINK_ARCHIVE_CONTENT_TEMPLATES:
        render_and_write(template, ENV.get_template(template, globals=data))


def construct_global_data(config):
    """ Create the global template variables """
    return {
        'timezone': config['timezone'],
        'now': datetime.datetime.now(pytz.timezone(config['timezone'])),
        'index_refresh_interval': config.get('PAGE_REFRESH_INTERVAL_SECONDS'),
        'internal_pages': {
            'about': 'about.html',
            'archive': 'archive.html',
            'contribute': 'contribute.html',
            'main': 'index.html',
            'subscribe': 'subscribe.html',
        },
        'ENABLE_GOOGLE_ADS': config.getboolean('ENABLE_GOOGLE_ADS'),
        'ENABLE_GOOGLE_LINK_TRACKING': config.getboolean('ENABLE_GOOGLE_LINK_TRACKING'),
        'ENABLE_TAGS': config.getboolean('ENABLE_TAGS'),
        'ENABLE_LINK_NETLOC': config.getboolean('ENABLE_LINK_NETLOC'),
        'ENABLE_AUTOREFRESH': config.getboolean('ENABLE_AUTOREFRESH'),
        'reply_to_address': config['reply_to_address'],
    }
