#!/usr/bin/env bash
# Daily Grower Site Build Script

# Install app dependencies
export PYTHONPATH=`pwd`

# Prime build environment
export OUTPUT_DIR=output
rm -rf ${OUTPUT_DIR} && mkdir -p ${OUTPUT_DIR}/static
cp -r static/* ${OUTPUT_DIR}/static

# Go on, Build it
echo "Executing ${BUILD_TYPE}-type build " `date`
python3 build.py
