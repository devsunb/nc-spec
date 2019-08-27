#!/bin/bash
export GOPT_ROOT=/mnt/e/g2gs/gopt
export GOPT_IMAGE_NAME=ade.kosc.kr:5000/g2gs-gopt

export GOPT_VERSION=`cat ${GOPT_ROOT}/VERSION`

cd ${GOPT_ROOT}
rm -rf dist docker/gopt-*-py3-none-any.whl docker/run.py
python setup.py bdist_wheel && \
  mv dist/gopt-${GOPT_VERSION}-py3-none-any.whl docker/
cp gopt/run.py docker/

cd docker/
docker build -t ${GOPT_IMAGE_NAME}:${GOPT_VERSION} . && \
  docker push ${GOPT_IMAGE_NAME}:${GOPT_VERSION}
