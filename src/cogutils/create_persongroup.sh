#!/bin/sh

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
. $cwd/../cognitive.conf

if [ $# -ne 2 ]
then
    echo "Usage: $0 <personGroupId> <groupName>"
    exit 1
fi

PERSON_GROUP_ID=$1
PERSON_GROUP_NAME=$2

URL="https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/$PERSON_GROUP_ID"

curl -s \
 -H "Content-Type: application/json" \
 -H "Ocp-Apim-Subscription-Key: $SUBKEY" \
 -XPUT $URL -d"{
    \"name\":\"$PERSON_GROUP_NAME\",
    \"userData\":\"user-provided data attached to the person group\"
}"
