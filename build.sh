#!/usr/bin/env bash
if [ "$DIFFTREE" == "piggypal" ]
then
    echo "Skipping java build"
else
  mvn install -DskipTests=true -Dmaven.javadoc.skip=true -B -V
fi