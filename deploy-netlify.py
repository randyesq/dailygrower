#!/usr/bin/env python3
"""
Main deploy entrance for the Daily Grower site on Netlify
"""
import datetime
import hashlib
import os
import pathlib
import pprint
import urllib.parse

import requests

SITE_ID = os.environ.get('NETLIFY_SITE_ID')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'output')
API_TOKEN = os.environ.get('NETLIFY_PERSONAL_ACCESS_TOKEN')
BRANCH = os.environ.get('BRANCH', 'main')

NETLIFY_SITE_DEPLOYS_BASE_URL = "https://api.netlify.com/api/v1/sites/{}/deploys".format(SITE_ID)
NETLIFY_SITE_DEPLOYS_RESTORE_URL = "https://api.netlify.com/api/v1/sites/{}/deploys/{}/restore"
NETLIFY_DEPLOY_FILES_BASE_URL = "https://api.netlify.com/api/v1/deploys/{}/files/{}"


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


if __name__ == "__main__":

    # Loop through the output files and get their SHA for deployment comparison
    deploy_files = {}
    deploy_sha1_fullpath = {}
    deploy_sha1_relpath = {}
    for path, subdirs, files in os.walk(OUTPUT_DIR):
        for name in files:
            fullpath = pathlib.PurePath(path, name)
            key = fullpath.relative_to(*fullpath.parts[:1])

            sha1 = hashlib.sha1()
            with open(fullpath, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    sha1.update(data)
            sha1str = sha1.hexdigest()
            deploy_files[urllib.parse.quote('/'+str(key))] = sha1str
            deploy_sha1_fullpath[sha1str] = str(fullpath)
            deploy_sha1_relpath[sha1str] = str(urllib.parse.quote('/'+str(key)))

    pprint.pprint(deploy_files)
    pprint.pprint(deploy_sha1_fullpath)
    pprint.pprint(deploy_sha1_relpath)

    # Call Netlify and propose the new deploy using the file-digest method
    auth = BearerAuth(API_TOKEN)
    deploy_response = requests.post(
        NETLIFY_SITE_DEPLOYS_BASE_URL,
        json={
            'files': deploy_files,
            'functions': None,
            'title': 'github render deploy @ %s' % datetime.datetime.now(),
            'branch': BRANCH
        },
        auth=auth,
    )
    print(deploy_response.text)
    deploy_response.raise_for_status()

    # For every file that Netlify wants, upload it
    deploy_id = deploy_response.json()['id']
    print("deploy id=%s" % deploy_id)
    for reqd_sha1 in deploy_response.json()['required']:
        print("Uploading", deploy_sha1_fullpath[reqd_sha1])
        with open(deploy_sha1_fullpath[reqd_sha1], 'rb') as payload:
            upload_response = requests.put(
                NETLIFY_DEPLOY_FILES_BASE_URL.format(deploy_id, deploy_sha1_relpath[reqd_sha1]),
                auth=auth,
                data=payload
            )
            print(upload_response.text)
            upload_response.raise_for_status()

    # I guess everything went fine, so update the deploy to be published
    publish_response = requests.post(
        NETLIFY_SITE_DEPLOYS_RESTORE_URL.format(SITE_ID, deploy_id),
        auth=auth,
        json={}
    )
    print(publish_response.text)
    publish_response.raise_for_status()
