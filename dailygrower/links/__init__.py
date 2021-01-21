from datetime import datetime
from urllib.parse import urlparse, parse_qsl


def fetch_youtube_images(links):
    """
    If the link is a youtube video, fetch its youtube thumbnail image
    # https://stackoverflow.com/questions/2068344/how-do-i-get-a-youtube-video-thumbnail-from-the-youtube-api
    """
    for link in links:
        if 'youtu' in link['netloc']:
            query = urlparse(link['fields']['Link']).netloc
            vid = dict(parse_qsl(urlparse(link['fields']['Link']).query))['v']
            link['image'] = "https://i.ytimg.com/vi/{}/hqdefault.jpg".format(vid)
        else:
            link['image'] = None
    return links