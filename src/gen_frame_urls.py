#!/usr/bin/env python
# -*- coding: utf-8 -*-

########### Python 2.7 #############
import sys
import os
import json
import httplib, urllib, base64
import csv
from libs import storage
from libs import config

config_file = 'storage.conf'

def usage(c):
    print 'Usage: # python %s <storage_container> <urlsfile:out>' % c

if __name__ == '__main__':
    # add python running path
    sd = os.path.dirname(__file__)
    sys.path.append(sd)

    argvs = sys.argv
    argc = len(argvs)
    if (argc !=3 ):
        usage(argvs[0])
        quit()
    container_name = argvs[1]
    out_frameurls = argvs[2]

    config = config.read_config(config_file)
    try:
        wf = open(out_frameurls, 'w')
        api = storage.BlobStorageContainer(
                config["ACCOUNT_NAME"],config["ACCOUNT_KEY"],container_name)
        frame_image_blobs = api.get_blobs_list('jpg')
        for frame_image in frame_image_blobs:
            line = "http://{0}.blob.core.windows.net/{1}/{2}\n".format(
                        config["ACCOUNT_NAME"], container_name, frame_image)
            wf.write(line)
    except IOError:
        print('Cannot Open {}'.format(out_frameurls))
    except Exception as e:
        print ("Exception occurd during storage api execution!")
    else:
        wf.close
