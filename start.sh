#!/usr/bin/env bash

BASE=/home/deploy/webhook

#source ${BASE}/.venv/bin/activate
${BASE}/.venv/bin/python serve.py > /mnt/log/serve.log 2>&1
