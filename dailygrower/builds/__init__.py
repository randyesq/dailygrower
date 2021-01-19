# Daily Grower Build Types
import os

from dailygrower.airtable import LinksAirtableView, get_next_link
from dailygrower.render import render_full_site

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')


def deploy_weekday(config):
    """ Deploy a weekday site """
    link_content = _get_link_views(config, True, True, True)

    # Get the next link to be featured this week
    next_link = get_next_link(link_content['pending'].get_view_records())

    # Update that link to be current
    if next_link:
        link_content['pending'].approve_record(next_link)

    # Render Site
    render_full_site(config, link_content=link_content)

    # Create subscriber email
    #send_daily_link_email(next_link)


def deploy_rollup(config):
    """ Deploy a rollup site, typically a Saturday """
    link_content = _get_link_views(config, archived=True)

    # Render Site
    render_full_site(config, link_content=link_content)

    # Create subscriber email
    #send_weekly_rollup_link_email(next_link)


def deploy_sabbath(config):
    """ Deploy a sabbath site, typically a Sunday """
    link_content = _get_link_views(config, archived=True)

    # Render Site
    render_full_site(config, link_content=link_content)

    # Archive this week's posts
    #archive_current_posts(config, current)


def _get_link_views(config, pending=False, current=True, archived=False):
    """ Get the content table views as prescribed """
    link_content = {}
    if pending:
        link_content['pending'] = LinksAirtableView(
            config['base_id'], config['content_table'], config['pending_view'], AIRTABLE_API_KEY
        )

    if current:
        link_content['current'] = LinksAirtableView(
            config['base_id'], config['content_table'], config['current_view'], AIRTABLE_API_KEY
        )

    if archived:
        link_content['archived'] = LinksAirtableView(
            config['base_id'], config['content_table'], config['archived_view'], AIRTABLE_API_KEY
        )

    return link_content