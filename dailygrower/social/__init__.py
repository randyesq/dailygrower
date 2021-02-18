# Routines for posting to social media
import os

import facebook
import datetime


def create_facebook_post(config, next_link):
    """ Create a facebook post on the Daily Grower Page """
    fb_page = config['facebook_page_id']
    access_token = os.environ.get("FACEBOOK_ACCESS_TOKEN")
    graph = facebook.GraphAPI(access_token=access_token, version="2.12")
    then = datetime.datetime.now() + datetime.timedelta(hours=1)
    link = next_link[0]
    message = """
    Today on The Daily Grower:

    {} --- {}

    Read more at https://dailygrower.com
    """.format(link.headline, link.blurb)
    print(graph.put_object(
        fb_page,
        "feed",
        published=False,
        message=message,
        scheduled_publish_time=then.replace(microsecond=0).isoformat()
    ))
