#!/bin/sh

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
. $cwd/../cognitive.conf

if [ $# -ne 1 ]
then
    echo "Usage: $0 <personGroupId>"
    exit 1
fi

PERSON_GROUP_ID=$1

URL="https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/$PERSON_GROUP_ID/persons"

{
curl -s \
 -H "Content-Type: application/json" \
 -H "Ocp-Apim-Subscription-Key: $SUBKEY" \
 -XGET $URL
} | python -mjson.tool| perl -Xpne 's/\\u([0-9a-fA-F]{4})/chr(hex($1))/eg'
