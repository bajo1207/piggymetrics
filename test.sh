#!/usr/bin/env bash
if ["$DIFFTREE" == "piggypal"]; then
    echo "Skipping java test"
else
  mvn test -B
fi