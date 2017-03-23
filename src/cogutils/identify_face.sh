#!/bin/sh

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
. $cwd/../cognitive.conf

URL="https://westus.api.cognitive.microsoft.com/face/v1.0/identify"

if [ $# -ne 2 ]
then
    echo "Usage: $0 <personGroupId> <faceId>"
    exit 1;
fi

PERSON_GROUP_ID=$1
FACE_ID=$2

{
curl -s \
 -H "Content-Type: application/json" \
 -H "Ocp-Apim-Subscription-Key: $SUBKEY" \
 -XPOST $URL -d"{
    \"personGroupId\":\"$PERSON_GROUP_ID\",
    \"faceIds\":[
        \"$FACE_ID\"
    ],
    \"maxNumOfCandidatesReturned\":1,
    \"confidenceThreshold\": 0.5
}"
}  | python -mjson.tool| perl -Xpne 's/\\u([0-9a-fA-F]{4})/chr(hex($1))/eg'
