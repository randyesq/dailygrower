import datetime
import math
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
import pytz

from dailygrower.airtable import fetch_links, get_link_tags
from dailygrower.links import weight_links, parse_netloc, fetch_youtube_images

template_name = os.environ.get('TEMPLATE_NAME', 'index.html.j2')
fetch_links_from_db = os.environ.get('FETCH_LINKS', False)
output_dir = Path(os.environ.get('OUTPUT_DIR', Path(__file__).parent.parent.joinpath('output')))

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent.parent.joinpath('templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# Fetch the links and advertisements from the database
links = []
ads = []
if fetch_links_from_db:
    if template_name == "index.html.j2":
        links = fetch_links(view="Live", table="Content")
        ads = fetch_links(view="Live", table="Advertisements")
    elif template_name == "archive.html.j2":
        links = fetch_links(view="Archived", table="Content")
    links = weight_links(links)
    links = parse_netloc(links)
    links = fetch_youtube_images(links)

# Pagination
if template_name == "index.html.j2":
    links_per_page = 5
    link_pagination_pages = math.ceil(len(links) / links_per_page)
elif template_name == "archive.html.j2":
    links_per_page = 10
    link_pagination_pages = math.ceil(len(links) / links_per_page)
    links.sort(key=lambda x: x['fields']['Approval Date'], reverse=True)
else:
    links_per_page = None
    link_pagination_pages = None


# Get the date in the CST/CDT timezone
tz = pytz.timezone('America/Chicago')

# Template variables
template_globals = {
    'now': datetime.datetime.now(tz),
    'index_refresh_interval': 24*60*60 + 10*60,  # 24 hours plus 10 minutes
    'links': links,
    'ads': ads,
    'tags': get_link_tags(links),
    'links_per_page': links_per_page,
    'link_pagination_pages': link_pagination_pages,
    'subscribe_url': 'subscribe.html',
    'TEMPLATE_NAME': template_name,
    'ENABLE_GOOGLE_ADS': True,
    'ENABLE_GOOGLE_LINK_TRACKING': True,
    'ENABLE_TAGS': False,
    'ENABLE_LINK_NETLOC': True,
    'ENABLE_LINK_SCORE_DISPLAY': False,
    'ENABLE_AUTOREFRESH': True,
}

# Render the templates
template = env.get_template(template_name, globals=template_globals)

# Write the template file (removing the .j2 extension) to the output_dir
with open(str(output_dir/Path(template_name).stem), 'w') as template_output_file:
    template_output_file.write(template.render())