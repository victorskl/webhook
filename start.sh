#!/usr/bin/env bash

BASE=/home/deploy/webhook

#source ${BASE}/.venv/bin/activate
#${BASE}/.venv/bin/python serve.py > /mnt/log/serve.log 2>&1
${BASE}/.venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 serve:app --chdir=${BASE} > /mnt/log/serve.log 2>&1
