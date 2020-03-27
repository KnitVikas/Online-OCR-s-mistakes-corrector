#!/bin/sh

lastUpdate=$(date -r /tmp/health +%s)
now=$(date +%s)
diff=$((now - lastUpdate))

if [ "$diff" -lt 20 ];
then
    echo "0"
else
    echo "1"
fi
