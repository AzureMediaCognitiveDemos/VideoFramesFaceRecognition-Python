#!/usr/bin/env python
# -*- coding: utf-8 -*-

########### Python 2.7 #############
import sys
import json
import httplib, urllib, base64
import time
import csv
from libs import faceapi
from libs import personsdb
from libs import storage
from libs import webvtt
from libs import config

config_file = 'cognitive.conf'
MAX_RETRY_COUNT=2

def usage(c):
    print 'Usage: # python %s <persongroup_id> <face_url_list> <master_csv> <output_webvtt>' % c

class IDAssigner:
    def __init__(self):
        self.__counter = 0 
        self.__hash = {}
 
    def get_assigned_id(self,name):
        if self.__hash.has_key(name):
            return self.__hash[name]
        else:
            self.__counter = self.__counter + 1
            self.__hash[name] = "FACE{0}".format(self.__counter)
            return self.__hash[name]

    def get_assigned_ids(self,names):
        assigned_ids =[]
        for name in names:
            assigned_ids.append(self.get_assigned_id(name))            
        return assigned_ids


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 5):
        usage(argvs[0])
        quit()
    sec_counter=0

    persongroup_id = argvs[1]
    face_url_list_file = argvs[2]
    master_csv_file = argvs[3]
    output_webvtt_file = argvs[4]

    config = config.read_config(config_file)
    webvtt = webvtt.WebvttWriter(output_webvtt_file)
    idassigner = IDAssigner()
    personsdb = personsdb.PersonsCSVDB(master_csv_file)
    personsdb.dump()

    api = faceapi.CognitiveServices_FaceAPI(config["SUBKEY"])
    rf = open(face_url_list_file)
    face_url = rf.readline().strip()
    sec_counter=sec_counter+1
    while face_url:

        print "face_url => "  + face_url
        ######### find similar ##########
        faceIdList = []
        resultDict = {}
        retry_count = 0
        while True:
            try:
                faceIdList = api.detect_face(face_url)
                if len(faceIdList) > 0:
                    resultDict = api.identify_personfaces(persongroup_id,faceIdList)
                break
            except Exception as e:
                print ("Exception occurd during api execution retry({0})".format(retry_count))
                retry_count += 1
                if retry_count > MAX_RETRY_COUNT:
                    sys.exit()

        if not resultDict:
            print "No personfaces were identified! for url: %s" % face_url
            sec_counter=sec_counter+1
            face_url = rf.readline().strip()
            continue

        detected_persons = []
        for faceId,candidates in resultDict.iteritems():
            if len(candidates) < 1:
                # detected but person not found in the list
                detected_persons.append(idassigner.get_assigned_id(faceId))
            else: 
                # found person in pre registered persongroup!
                # try to find until find the one in personsdb
                found_person_name_in_master = ''
                confidence = 0
                for candidate in candidates:
                    if candidate and candidate.has_key("personId"):
                        n = personsdb.get_name(candidate['personId'])
                        print "found person name:%s" % n
                        # if found_person_name_in_master is empty, simply assign first identified person
                        if not found_person_name_in_master:
                            found_person_name_in_master = n
                            confidence = candidate['confidence']
                        # if it's in master, assign the identified person and break
                        if personsdb.is_master(candidate['personId']):
                            print "this person was actually in master:%s" % n
                            found_person_name_in_master = n
                            confidence = candidate['confidence']
                            break
                if found_person_name_in_master:
                    s = "{0}({1})".format(found_person_name_in_master,confidence)
                    print s
                    detected_persons.append(s)
                else:
                    detected_persons.append(idassigner.get_assigned_id(faceId))
        ######### //find similar ##########
        #print 'detected_persons count=',len(detected_persons)
        #print 'detected_persons=',detected_persons
        if len(detected_persons) > 0:
            #print 'start sec_counter=',sec_counter
            #print 'end sec_counter=',sec_counter+1
            #print 'line=',' '.join(detected_persons)
            webvtt.write_webvtt_line(sec_counter, sec_counter+1, ' '.join(detected_persons))

        face_url = rf.readline().strip()
        sec_counter=sec_counter+1
        time.sleep(1.0) # sec

    rf.close
