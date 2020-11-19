import datetime
import math
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
import pytz

from dailygrower.airtable import fetch_links, get_link_tags
from dailygrower.links import weight_links, parse_netloc

template_name = os.environ.get('TEMPLATE_NAME', 'index.html.j2')
fetch_links_from_db = os.environ.get('FETCH_LINKS', False)
output_dir = Path(os.environ.get('OUTPUT_DIR', Path(__file__).parent.parent.joinpath('output')))

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent.parent.joinpath('templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

LINKS_PER_PAGE = 5

# Fetch the links and advertisements from the database
links = []
ads = []
if fetch_links_from_db:
    links = fetch_links(view="Live", table="Content")
    ads = fetch_links(view="Live", table="Advertisements")
    links = weight_links(links)
    links = parse_netloc(links)


# Get the date in the CST/CDT timezone
tz = pytz.timezone('America/Chicago')

# Template variables
template_globals = {
    'now': datetime.datetime.now(tz),
    'index_refresh_interval': 24*60*60 + 10*60,  # 24 hours plus 10 minutes
    'links': links,
    'ads': ads,
    'tags': get_link_tags(links),
    'links_per_page': LINKS_PER_PAGE,
    'link_pagination_pages': math.ceil(len(links) / LINKS_PER_PAGE),
    'subscribe_url': 'subscribe.html',
    'ENABLE_GOOGLE_ADS': False,
    'ENABLE_GOOGLE_LINK_TRACKING': True,
    'ENABLE_TAGS': False,
    'ENABLE_LINK_NETLOC': True,
    'ENABLE_LINK_SCORE_DISPLAY': False,
    'ENABLE_AUTOREFRESH': True,
}

template = env.get_template(template_name, globals=template_globals)

# Write the template file (removing the .j2 extension) to the output_dir
with open(str(output_dir/Path(template_name).stem), 'w') as template_output_file:
    template_output_file.write(template.render())