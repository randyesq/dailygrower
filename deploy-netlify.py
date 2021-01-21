#!/usr/bin/env python3
"""
Main deploy entrance for the Daily Grower site on Netlify
"""
import os
import tarfile

from google.cloud import storage

# Authenticate
gcs_key = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
branch = os.environ.get('BRANCH', 'main')
storage_client = storage.Client.from_service_account_json(gcs_key)

# Download and extract the tar file
bucket = storage_client.bucket(bucket_name="dailygrower-site")
blob = bucket.blob(branch+'/site.tar')
blob.download_to_filename('site.tar')

with tarfile.open('site.tar', 'r') as tar:
    tar.extractall()
