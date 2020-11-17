#!/usr/bin/env bash

export OUTPUT_DIR=output
export PYTHONPATH=`pwd`

rm -rf ${OUTPUT_DIR} && mkdir -p ${OUTPUT_DIR}/static
pip3 install -r requirements.txt
cp -r static/* ${OUTPUT_DIR}/static
TEMPLATE_NAME=index.html.j2 python3 controllers/index.py
TEMPLATE_NAME=submit.html.j2 python3 controllers/index.py
TEMPLATE_NAME=subscribe.html.j2 python3 controllers/index.py
TEMPLATE_NAME=contrib-thanks.html.j2 python3 controllers/index.py
