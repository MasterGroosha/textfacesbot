#!/bin/bash

# cd to script directory
cd "$(dirname "$0")" || exit 1

# check faces.txt file and copy if it doesn't exist in /app/data/
FACES_FILE="/app/data/faces.txt"
if [ ! -f "$FACES_FILE" ]; then
  cp faces_original.txt "$FACES_FILE"
fi

# start bot
python textfacesbot.py
