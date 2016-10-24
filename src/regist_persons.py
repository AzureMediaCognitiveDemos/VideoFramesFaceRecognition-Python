#!/usr/bin/env python
# -*- coding: utf-8 -*-

########### Python 2.7 #############
import sys
import os
import json
import httplib, urllib, base64
import csv
from libs import faceapi
from libs import config

config_file = 'cognitive.conf'

MAX_PERSON_NUM=1000

def usage(c):
    print 'Usage: # python %s <persongroup_id> <csvfile:in> <csvfile:out>' % c

if __name__ == '__main__':
    # add python running path
    sd = os.path.dirname(__file__)
    sys.path.append(sd)

    argvs = sys.argv
    argc = len(argvs)
    if (argc !=4 ):
        usage(argvs[0])
        quit()
    persongroup_id = argvs[1]
    in_csvfile= argvs[2]
    out_csvfile = argvs[3]

    config = config.read_config(config_file)

    wf = open(out_csvfile, 'ab')
    csvWriter = csv.writer(wf)
    api = faceapi.CognitiveServices_FaceAPI(config["SUBKEY"])
    person_counter = 0

    created_person_hash = {} # key:person_name / val:person_id

    with open(in_csvfile, 'r') as rf:
        reader = csv.reader(rf)
        #next(reader)   # skip header
        # url,facename
        for col in reader:
            face_url=col[0]
            person_name=col[1]
            master_flag=col[2]
            
            ## create person if not exists and get person_id
            person_id = ''
            if (created_person_hash.has_key(person_name)):
                person_id = created_person_hash[person_name]
            else:
                if (person_counter >= MAX_PERSON_NUM ):
                    print "WARN: persons reaced max:%d! you cannot add any more" % MAX_PERSON_NUM
                    break
                person_id = api.create_person(persongroup_id,person_name)
                person_counter +=1
                print 'created person: person_id (%d) => %s' % ( person_counter, person_id )
                created_person_hash[person_name] = person_id
                ### Wrightign row to CSV output file      
                wcols = []
                wcols.append(person_name) 
                wcols.append(person_id) 
                wcols.append(master_flag) 
                csvWriter.writerow(wcols)

            ## add personface to person
            persisted_face_id = api.add_personface_to_person(persongroup_id, person_id, face_url)
            if not persisted_face_id:
                print "ERR: failed to added face_url:{0} to person:{1}".format(face_url,person_name)
                continue
    wf.close
    
    # train
    api.train_persongroup(persongroup_id)

