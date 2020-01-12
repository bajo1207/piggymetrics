#!/usr/bin/env bash
if [ "$GREPPAL" == "piggypal" ]
then
    echo "Starting piggypal tests"
    cd ./piggypal/src/main
    python -m pytest
fi