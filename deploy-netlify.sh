#!/usr/bin/env bash
# Daily Grower Deploy Script

# Install app dependencies
export PYTHONPATH=`pwd`
pip3 install -r requirements-netlify.txt

# Prime environment
echo "${NETLIFY_DEPLOY_GCP_SA_KEY}" >> key.json
export GOOGLE_APPLICATION_CREDENTIALS="key.json"
export OUTPUT_DIR=output
rm -rf ${OUTPUT_DIR} && mkdir -p ${OUTPUT_DIR}

# Set the deploy type, default to the production config
if [ -z ${INCOMING_HOOK_BODY+x} ]; then
    export BRANCH="main"
else
    export BRANCH=`echo $INCOMING_HOOK_BODY | jq -r .BRANCH`
fi

# Go on, deploy it
python3 ./deploy-netlify.py
