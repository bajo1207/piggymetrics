#!/usr/bin/env bash
if [ "$GREPPAL" == "piggypal" ]
then
    echo "Starting piggypal tests"
    pip install pytest, requests, requests-oauthlib, cherrypy, oauthlib, re, contextlib
    cd /piggypal/src/main
    python -m pytest
fi

if [ "$DIFFTREE" != "piggypal" ]
then
    echo "Starting piggymetrics tests"
    mvn test -B
fi
