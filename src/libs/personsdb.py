########### Python 2.7 #############
import sys
import csv

class PersonsCSVDB:
    def __init__(self, master_csv):
         self.__hash = {}
         self.__load_csv(master_csv)
    
    def __load_csv(self, master_csv_file):
        with open(master_csv_file, 'r') as rf:
            reader = csv.reader(rf)
            # url,facename
            for col in reader:
                person_name=col[0]
                person_id=col[1]
                master_flag=col[2]
                ##print "load: ( person_id, person_name ) = ( {0}, {1} )".format(person_id,person_name)
                if person_name and person_id:
                    self.__hash[person_id] = [person_name, master_flag]

    def get_name(self,id):
        name = ''
        if (self.__hash.has_key(id)):
            name = self.__hash[id][0]
        return name

    def is_master(self,id):
        if (self.__hash.has_key(id)):
            if int(self.__hash[id][1]) > 0:
                return True
        return False

    def dump(self):
        for k, v in self.__hash.iteritems():
            print "dump key: %s,\t value:%s" %(k, v)
