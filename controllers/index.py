import datetime
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from dailygrower.airtable import fetch_links

template_name = os.environ.get('TEMPLATE_NAME', 'index.html.j2')
output_dir = Path(os.environ.get('OUTPUT_DIR', Path(__file__).parent.parent.joinpath('output')))

env = Environment(
    loader=FileSystemLoader(
        Path(__file__).parent.parent.joinpath('templates')
    ),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

globals = {
    'now': datetime.datetime.now(),
    'links': fetch_links()['records'],
}

template = env.get_template(template_name, globals=globals)

# Write the template file (removing the .j2 extension) to the output_dir
with open(str(output_dir/Path(template_name).stem), 'w') as template_output_file:
    template_output_file.write(template.render())