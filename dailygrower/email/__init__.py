# Daily Grower Email Package
import datetime
import os
import requests
from dailygrower.render import ENV, construct_global_data

BUTTONDOWN_API_KEY = os.environ.get("BUTTONDOWN_API_KEY")


def send_daily_link_email(config, links, deals_content):
    """ Use buttondown to send an email with today's freshest link """
    data = construct_global_data(config)
    data['links'] = links
    today_new_deals = []
    for deal in deals_content.get_view_records():
        if deal.available_date == datetime.datetime.today().date():
            today_new_deals.append(deal)

    data['deals'] = today_new_deals
    template = ENV.get_template("daily_digest.md.j2", globals=data)

    # Send the email via Buttondown API to daily subscribers
    subject = "{} -- today on The Daily Grower".format(links[0].headline)
    r = requests.post(
        config['buttondown_api_base_url']+'emails',
        json={
            "body": template.render(),
            "included_tags": [ config['daily_digest_subscriber_tag'] ],
            "email_type": "public",
            "external_url": "https://dailygrower.com",
            "slug": "daily-{}".format(data['now'].strftime("%Y-%m-%d")),
            "subject": subject,
        },
        headers={"Authorization": "Token %s" % BUTTONDOWN_API_KEY}
    )
    print(r.text)
    r.raise_for_status()
    print("Email creation response to daily subscribers: %s" % r.json())

    # Send the email via Buttondown API to all digest subscribers
    r = requests.post(
        config['buttondown_api_base_url']+'emails',
        json={
            "body": template.render(),
            "included_tags": [ config['all_digests_subscriber_tag']  ],
            "email_type": "public",
            "external_url": "https://dailygrower.com",
            "slug": "daily-{}".format(data['now'].strftime("%Y-%m-%d")),
            "subject": subject+"!"
        },
        headers={"Authorization": "Token %s" % BUTTONDOWN_API_KEY}
    )
    print(r.text)
    r.raise_for_status()
    print("Daily email creation response to all-digest subscribers: %s" % r.text)


def send_weekly_rollup_email(config, links, deals_content):
    """ Use buttondown to send an email with this week's links """
    data = construct_global_data(config)
    data['links'] = links
    new_deals = []
    today = datetime.datetime.today().date()
    for deal in deals_content.get_view_records():
        days_available = today - deal.available_date
        if days_available.days <= 7 and days_available.days >= 0:
            new_deals.append(deal)

    data['deals'] = new_deals
    template = ENV.get_template("weekly_digest.md.j2", globals=data)

    # Send the email via Buttondown API to weekly subscribers
    r = requests.post(
        config['buttondown_api_base_url']+'emails',
        json={
            "body": template.render(),
            "included_tags": [ config['weekly_digest_subscriber_tag'] ],
            "email_type": "public",
            "external_url": "https://dailygrower.com",
            "slug": "weekly-{}".format(data['now'].strftime("%Y-%m-%d")),
            "subject": "Your stories for this week from The Daily Grower"
        },
        headers={"Authorization": "Token %s" % BUTTONDOWN_API_KEY}
    )
    print(r.text)
    r.raise_for_status()
    print("Weekly email creation response: %s" % r.json())

    # Send the email via Buttondown API to all digest subscribers
    r = requests.post(
        config['buttondown_api_base_url']+'emails',
        json={
            "body": template.render(),
            "included_tags": [ config['all_digests_subscriber_tag'] ],
            "email_type": "public",
            "external_url": "https://dailygrower.com",
            "slug": "weekly-{}".format(data['now'].strftime("%Y-%m-%d")),
            "subject": "Your stories for this week from The Daily Grower!"
        },
        headers={"Authorization": "Token %s" % BUTTONDOWN_API_KEY}
    )
    print(r.text)
    r.raise_for_status()
    print("Weekly email creation response to all-digest subscribers: %s" % r.json())
