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

URL="https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/$PERSON_GROUP_ID/train"

{
curl -s \
 -H "Content-Type: application/json" \
 -H "Ocp-Apim-Subscription-Key: $SUBKEY" \
 -XPOST $URL -d ""
}
