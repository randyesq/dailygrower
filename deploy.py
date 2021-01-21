#!/usr/bin/env python3
"""
Main deploy entrance for the Daily Grower site
"""
import configparser
import os

from dailygrower.builds import deploy_rollup, deploy_sabbath, \
    deploy_weekday, deploy_render

# Gather build and deploy types from the environment
BUILD_TYPE = os.environ.get("BUILD_TYPE", "weekday")
DEPLOY_TYPE = os.environ.get("DEPLOY_TYPE", "production")

# Read in the environment configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Call the build function based on the build type with the config
# based on the deploy type
globals()['deploy_'+BUILD_TYPE](config[DEPLOY_TYPE])
