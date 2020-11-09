import datetime
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from dailygrower.airtable import fetch_links, get_link_tags
from dailygrower.links import weight_links

template_name = os.environ.get('TEMPLATE_NAME', 'index.html.j2')
output_dir = Path(os.environ.get('OUTPUT_DIR', Path(__file__).parent.parent.joinpath('output')))

env = Environment(
    loader=FileSystemLoader(
        Path(__file__).parent.parent.joinpath('templates')
    ),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# Fetch the links from the database
links = fetch_links(view="Live", table="Content")
links = weight_links(links)

# Template variables
template_globals = {
    'now': datetime.datetime.now(),
    'links': links,
    'tags': get_link_tags(links)
}

template = env.get_template(template_name, globals=template_globals)

# Write the template file (removing the .j2 extension) to the output_dir
with open(str(output_dir/Path(template_name).stem), 'w') as template_output_file:
    template_output_file.write(template.render())