#!/usr/bin/env bash

export OUTPUT_DIR=output
export PYTHONPATH=`pwd`

rm -rf ${OUTPUT_DIR} && mkdir -p ${OUTPUT_DIR}/static
pip3 install -r requirements.txt
cp -r static/* ${OUTPUT_DIR}/static
echo "Rendering template: index.html.j2"
TEMPLATE_NAME=index.html.j2 FETCH_LINKS=true python3 controllers/index.py
echo "Rendering template: archive.html.j2"
TEMPLATE_NAME=archive.html.j2 FETCH_LINKS=true python3 controllers/index.py
for template in about.html.j2 contribute.html.j2 contrib-thanks.html.j2 subscribe.html.j2 subscribe-thanks.html.j2
do
    echo "Rendering template: ${template}"
    TEMPLATE_NAME=${template} python3 controllers/index.py
done
