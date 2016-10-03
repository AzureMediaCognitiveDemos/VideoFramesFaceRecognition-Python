#!/bin/sh

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
. $cwd/../cognitive.conf

if [ $# -ne 1 ]
then
    echo "Usage: $0 <face_url>"
    exit 1
fi

FACE_URL=$1

URL="https://api.projectoxford.ai/face/v1.0/detect"

curl -s \
 -H "Content-Type: application/json" \
 -H "Ocp-Apim-Subscription-Key: $SUBKEY" \
 -XPOST $URL -d"{
    \"url\":\"$FACE_URL\"
}"
