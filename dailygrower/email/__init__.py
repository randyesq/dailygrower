# Daily Grower Email Package
import os
import requests
from dailygrower.render import ENV, construct_global_data

BUTTONDOWN_API_KEY = os.environ.get("BUTTONDOWN_API_KEY")


def send_daily_link_email(config, links):
    """ Use buttondown to send an email with today's freshest link """
    data = construct_global_data(config)
    data['links'] = links
    template = ENV.get_template("daily_digest.md.j2", globals=data)

    # Send the email via Buttondown API
    r = requests.post(
        config['buttondown_api_base_url']+'emails',
        json={
            "body": template.render(),
            "included_tags": [ config['daily_digest_subscriber_tag'] ],
            "email_type": "public",
            "external_url": "https://dailygrower.com",
            "slug": "daily-{}".format(data['now'].strftime("%Y-%m-%d")),
            "subject": "Your stories for {} from The Daily Grower".format(data['now'].strftime("%A, %B %d"))
        },
        headers={"Authorization": "Token %s" % BUTTONDOWN_API_KEY}
    )
    r.raise_for_status()
    print("Daily email creation response %s" % r.text)


def send_weekly_rollup_email(config, links):
    """ Use buttondown to send an email with this week's links """
    data = construct_global_data(config)
    data['links'] = links
    template = ENV.get_template("weekly_digest.md.j2", globals=data)

    # Send the email via Buttondown API
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
    r.raise_for_status()
    print("Daily email creation response %s" % r.json())
