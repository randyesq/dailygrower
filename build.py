#!/usr/bin/env python3
"""
Main build entrance for the Daily Grower site
"""
import configparser
import os

from dailygrower.builds import build_rollup, build_sabbath, \
    build_weekday, build_render

# Gather build and deploy types from the environment
BUILD_TYPE = os.environ.get("BUILD_TYPE", "render").lower()
DEPLOY_TYPE = os.environ.get("DEPLOY_TYPE", "production").lower()

# Read in the environment configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Call the build function based on the build type with the config
# based on the deploy type
globals()['build_'+BUILD_TYPE](config[DEPLOY_TYPE])
