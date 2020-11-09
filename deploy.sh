#!/usr/bin/env bash

export OUTPUT_DIR=output
export PYTHONPATH=`pwd`

rm -rf ${OUTPUT_DIR} && mkdir -p ${OUTPUT_DIR}/static
pip3 install -r requirements.txt
cp static/* ${OUTPUT_DIR}/static
python3 controllers/index.py

