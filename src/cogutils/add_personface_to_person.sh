#!/bin/sh

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
. $cwd/../cognitive.conf

if [ $# -ne 3 ]
then
    echo "Usage: $0 <personGroupId> <personId> <face_url>"
    exit 1
fi

PERSON_GROUP_ID=$1
PERSON_ID=$2
FACE_URL=$3

URL="https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/$PERSON_GROUP_ID/persons/$PERSON_ID/persistedFaces"

curl -s \
 -H "Content-Type: application/json" \
 -H "Ocp-Apim-Subscription-Key: $SUBKEY" \
 -XPOST $URL -d"{
    \"url\":\"$FACE_URL\"
}"
