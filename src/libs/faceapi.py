########### Python 2.7 #############
import sys
import json
import httplib, urllib, base64
import time

class CognitiveServices_FaceAPI:
    def __init__(self, subkey):
        self.__subkey = subkey


    def train_persongroup(self, persongroup_id):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }
        params = urllib.urlencode({})
        REQ_BODY = ''
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/persongroups/{0}/train?{1}".format(persongroup_id, params),
                REQ_BODY, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return data


    def add_face_to_facelist(self,facelist_id, face_url, face_name=''):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }

        params = urllib.urlencode({
            # Request parameters
            'userData': face_name
        })
        ADDFACE_REQ_BODY = json.dumps( {"url":face_url}  ) 

        data = ''
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST",
                "/face/v1.0/facelists/{0}/persistedFaces?{1}".format(facelist_id,params), 
                ADDFACE_REQ_BODY, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return ''
        res=json.loads(data)
        #print res
        if isinstance(res, dict) and res.has_key('error'):
            print("[Error code:{0}] {1}".format(res['error']['code'], res['error']['message']))
            return '' 
        return res['persistedFaceId']
            

    def detect_face (self, face_url):
        faceIdList=[]
        faceattributes='age,gender,headPose,smile,facialHair,glasses'
    
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }

        params = urllib.urlencode({
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': faceattributes,
        })
        DETECT_REQ_BODY = json.dumps( {"url":face_url}  )
        data = ''
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/detect?%s" %
                            params, DETECT_REQ_BODY, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return faceIdList

        res=json.loads(data)
        for face in res:
            faceId = face['faceId']
            if faceId:
                faceIdList.append(faceId)
        return faceIdList


    def find_similar_faces(self,facelist_id,face_id_list):
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }
        params = urllib.urlencode({
        })

        returnDict = {}
        for face_id in face_id_list:
            FINDSIMILAR_REQ_BODY= json.dumps(
                        { 
                            "faceId":face_id,
                            "faceListId":facelist_id,
                            "maxNumOfCandidatesReturned":5
                        }
                    )
            data = ''
            try:
                conn = httplib.HTTPSConnection('api.projectoxford.ai')
                conn.request("POST", "/face/v1.0/findsimilars?%s" %
                                params, FINDSIMILAR_REQ_BODY, headers)
                response = conn.getresponse()
                data = response.read()
                returnDict[face_id] = json.loads(data)
                conn.close()
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
                returnDict[face_id] = {}
        return returnDict


    def print_similar_faces(self, facelist_id, face_url):
        face_id_list = []
        face_id_list = self.detect_face(face_url)
        resultDict = self.find_similar_faces(facelist_id,face_id_list)
        for face_id,results in resultDict.iteritems():
            #print 'faceId',face_id
            #print 'result',result
            rcount=0
            for result in results:
                print "faceId: {0} => similar#{1} persistedFaceId: {2} confidence: {3}".format(
                            face_id,
                            rcount,
                            result['persistedFaceId'], 
                            result['confidence']
                        )
                rcount=rcount+1


    def create_person (self, persongroup_id, person_name ):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }

        params = urllib.urlencode({})
        REQ_BODY = json.dumps({"name":person_name}) 
        data = ''
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST",
                "/face/v1.0/persongroups/{0}/persons?{1}".format(persongroup_id,params), 
                REQ_BODY, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return ''
        res=json.loads(data)
        #print res
        if isinstance(res, dict) and res.has_key('error'):
            print("[Error code:{0}] {1}".format(res['error']['code'], res['error']['message']))
            return '' 
        return res['personId']


    def get_person (self, persongroup_id, person_id ):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }
        params = urllib.urlencode({})
        REQ_BODY=''
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("GET", 
                "/face/v1.0/persongroups/{0}/persons/{1}?{2}".format(persongroup_id, person_id, params),
                    REQ_BODY , headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return ''
        res=json.loads(data)
        #print res
        if isinstance(res, dict) and res.has_key('error'):
            print("[Error code:{0}] {1}".format(res['error']['code'], res['error']['message']))
            return '' 
        return res


    def add_personface_to_person(self, persongroup_id, person_id, face_url):
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }
        params = urllib.urlencode({})
        REQ_BODY = json.dumps( {"url":face_url}  ) 
        data = ''
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST",
                "/face/v1.0/persongroups/{0}/persons/{1}/persistedFaces?{2}".format(persongroup_id, person_id, params), 
                REQ_BODY, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return ''
        res=json.loads(data)
        #print res
        if isinstance(res, dict) and res.has_key('error'):
            print("[Error code:{0}] {1}".format(res['error']['code'], res['error']['message']))
            return '' 
        return res['persistedFaceId']


    def identify_personfaces(self,persongroup_id, face_id_list):
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.__subkey,
        }
        params = urllib.urlencode({})
        bodies = { 
            "personGroupId": persongroup_id,
            "faceIds":face_id_list,
            "maxNumOfCandidatesReturned":5,
            "confidenceThreshold": 0.5
        }
        REQ_BODY= json.dumps(bodies)
        data = ''
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            conn.request("POST", "/face/v1.0/identify?%s" % params, REQ_BODY, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return ''
        res = json.loads(data)
        returnDict = {}
        if isinstance(res, dict) and res.has_key('error'):
            print("[Error code:{0}] {1}".format(res['error']['code'], res['error']['message']))
            return returnDict
        for result_face in res:
            if not result_face.has_key('faceId'):
                continue
            returnDict[result_face['faceId']] = result_face['candidates']
        return returnDict


    def print_identified_persons(self, persongroup_id, face_url):
        face_id_list = []
        resultDict = {} 
        face_id_list = self.detect_face(face_url)
        if len(face_id_list) > 0:
            resultDict = self.identify_personfaces(persongroup_id,face_id_list)
        if len(resultDict) < 1:
            print "No personfaces were identified!"
            sys.exit()
        for face_id,candidates in resultDict.iteritems():
            #print 'faceId',face_id
            #print 'result',result
            rcount=0
            for candidate in candidates:
                print "faceId: {0} => identified#{1} personId: {2} confidence: {3}".format(
                            face_id,
                            rcount,
                            candidate['personId'], 
                            candidate['confidence']
                        )
                rcount=rcount+1



if __name__ == '__main__': 
#    subkey='09883d1138ac485e88386e8e0c50ff3x' 
#    api = CognitiveServices_FaceAPI(subkey)
#
#    ### train person group
#    persongroup_id='testgroup' 
#    api.train_persongroup(persongroup_id)
#
#    ### facelist
#    # facelist_id='testmaster' 
#    # url = "http://yoichika-dev1.japanwest.cloudapp.azure.com/poc/nhk/poc3masterimages/okada.jpg"
#    # api.print_similar_faces(facelist_id,url)
#
#    ### person
#    #persongroup_id = 'testgroup'
#    #person_name = 'Yoichi Kawasaki'
#    #person_id = api.create_person(persongroup_id,person_name)
#    #print api.get_person(persongroup_id, person_id)
#
#    ### identify
#    persongroup_id = 'nhkpoc3case5'
#    url = 'http://yoichika-dev1.japanwest.cloudapp.azure.com/poc/nhk/poc3masterimages2/%E9%AB%98%E5%B1%B1%E4%B8%80%E5%AE%9F%EF%BC%88%E3%81%9F%E3%81%8B%E3%82%84%E3%81%BE%E3%81%8B%E3%81%9A%E3%81%BF%EF%BC%89.jpg'
#    api.print_identified_persons(persongroup_id, url) 

