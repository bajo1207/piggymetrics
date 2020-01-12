#!/usr/bin/env bash

if [ "$DIFFTREE" != "piggypal" ]
then
    echo "Starting piggymetrics tests"
    mvn test -B
fi