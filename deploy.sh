#!/usr/bin/env bash
# Daily Grower Build and Deploy Script

# Install app dependencies
export PYTHONPATH=`pwd`
pip3 install -r requirements.txt

# Set the build type, default to a weekday build
: "${BUILD_TYPE:=weekday}"

# Set the deploy type, default to the production config
: "${DEPLOY_TYPE:=production}"

# Prime build environment
export OUTPUT_DIR=output
rm -rf ${OUTPUT_DIR} && mkdir -p ${OUTPUT_DIR}/static
cp -r static/* ${OUTPUT_DIR}/static

# Go on, Build it
case ${BUILD_TYPE} in

    "weekday")
        echo "Executing weekday-type build " date
        python3 deploy.py
        ;;

    "rollup")
        echo "Executing rollup-type build " date
        ;;

    "sabbath")
        echo "Executing sabbath-type build " date
        ;;

esac
