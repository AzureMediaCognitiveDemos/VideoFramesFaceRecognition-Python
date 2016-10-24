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
    print 'Usage: # python %s <storage_container> <acl:0/1>' % c
    print '         acl: 0 - private, 1 - public'

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
    acl = int(argvs[2])
    if acl != 0 and acl !=1:
        usage(argvs[0])
        quit()
        
    config = config.read_config(config_file)
    try:
        api = storage.BlobStorageContainer(
                config["ACCOUNT_NAME"],config["ACCOUNT_KEY"],container_name)
        if acl == 1:
            api.set_container_acl_public()
        else:
            api.set_container_acl_private()
    except Exception as e:
        print ("Exception occurd during storage api execution!")
