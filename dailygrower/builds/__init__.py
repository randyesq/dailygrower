# Daily Grower Build Types
import os

from dailygrower.airtable import LinksAirtableView, get_next_link
from dailygrower.render import render_full_site
from dailygrower.email import send_daily_link_email


def build_render(config):
    """
    Render a site without making any automatic changes to links, just
    re-render the templates
    """
    link_content = _get_link_views(config, archived=True)

    # Render Site
    render_full_site(config, link_content=link_content)


def build_weekday(config):
    """
    Weekday build, pull a pending story off the shelf and send daily email
    """
    link_content = _get_link_views(config, True, True, True)

    # Get the next link to be featured this week
    next_link = get_next_link(link_content['pending'].get_view_records())

    # Update that link to be current
    if next_link:
        link_content['pending'].approve_records(next_link)

        # Create subscriber email
        send_daily_link_email(config, next_link)


def build_rollup(config):
    """ Rollup build, send weekly digest email """
    link_content = _get_link_views(config, archived=True)

    # Render Site
    render_full_site(config, link_content=link_content)

    # Create subscriber email
    #send_weekly_rollup_link_email(next_link)


def build_sabbath(config):
    """ Sabbath build, archive the previous week's posts, typically a Sunday """
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
            config['base_id'], config['content_table'], config['pending_view']
        )

    if current:
        link_content['current'] = LinksAirtableView(
            config['base_id'], config['content_table'], config['current_view']
        )

    if archived:
        link_content['archived'] = LinksAirtableView(
            config['base_id'], config['content_table'], config['archived_view']
        )

    return link_content