import datetime
import math
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from dailygrower.airtable import fetch_links, get_link_tags
from dailygrower.links import weight_links, parse_netloc

template_name = os.environ.get('TEMPLATE_NAME', 'index.html.j2')
output_dir = Path(os.environ.get('OUTPUT_DIR', Path(__file__).parent.parent.joinpath('output')))

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent.parent.joinpath('templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

LINKS_PER_PAGE = 5

# Fetch the links from the database
links = fetch_links(view="Live", table="Content")
ads = fetch_links(view="Live", table="Advertisements")
links = weight_links(links)
links = parse_netloc(links)

# Template variables
template_globals = {
    'now': datetime.datetime.now(),
    'links': links,
    'ads': ads,
    'tags': get_link_tags(links),
    'links_per_page': LINKS_PER_PAGE,
    'link_pagination_pages': math.ceil(len(links) / LINKS_PER_PAGE),
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