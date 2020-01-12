#!/usr/bin/env bash

echo "Starting piggypal tests"
pip3 install pytest, requests, requests-oauthlib, cherrypy, oauthlib, re, contextlib
cd ./piggypal/src/main
python -m pytest


