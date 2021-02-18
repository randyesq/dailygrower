# Daily Grower Build Types
import os

from dailygrower.airtable import LinksAirtableView, DealsLinkAirtableView, get_next_link
from dailygrower.render import render_full_site
from dailygrower.email import send_daily_link_email, send_weekly_rollup_email
from dailygrower.social import create_facebook_post


def build_render(config):
    """
    Render a site without making any automatic changes to links, just
    re-render the templates
    """
    link_content = _get_link_views(config, current=True, archived=True)
    deals_content = DealsLinkAirtableView(
        config['at_deals_base_id'],
        config['at_deals_table'],
        config['at_deals_view']
    )

    # Render Site
    render_full_site(
        config, link_content=link_content, deals_content=deals_content
    )


def build_weekday(config):
    """
    Weekday build, pull a pending story off the shelf and send daily email
    """
    link_content = _get_link_views(config, pending=True)

    # Get the next link to be featured this week
    next_link = get_next_link(link_content['pending'].get_view_records())

    # Update that link to be current
    if next_link:
        link_content['pending'].approve_records(next_link)
        deals_content = DealsLinkAirtableView(
            config['at_deals_base_id'],
            config['at_deals_table'],
            config['at_deals_view']
        )

        # Create daily digest subscriber email
        send_daily_link_email(config, next_link, deals_content)

        # Post to Facebook
        create_facebook_post(config, next_link)


def build_rollup(config):
    """ Rollup build, send weekly digest email, typically a Saturday """
    link_content = _get_link_views(config, current=True)
    deals_content = DealsLinkAirtableView(
        config['at_deals_base_id'],
        config['at_deals_table'],
        config['at_deals_view']
    )

    # Create weekly digest subscriber email
    send_weekly_rollup_email(
        config, link_content['current'].get_view_records(), deals_content
    )


def build_sabbath(config):
    """ Sabbath build, archive the previous week's posts, typically a Sunday """
    link_content = _get_link_views(config, current=True)

    # Archive this week's posts
    posts = link_content['current'].get_view_records()
    link_content['current'].archive_records(posts)


def _get_link_views(config, pending=False, current=False, archived=False):
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
