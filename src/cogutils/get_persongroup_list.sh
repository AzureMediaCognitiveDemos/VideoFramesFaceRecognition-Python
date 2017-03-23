#!/bin/sh

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
. $cwd/../cognitive.conf

START=0
TOP=1000

URL="https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups?start=$START&top=$TOP"

{
curl -s \
 -H "Content-Type: application/json" \
 -H "Ocp-Apim-Subscription-Key: $SUBKEY" \
 -XGET $URL
} | python -mjson.tool| perl -Xpne 's/\\u([0-9a-fA-F]{4})/chr(hex($1))/eg'
