########### Python 2.7 #############
import sys
#import json
#import httplib, urllib, base64
import time

class WebvttWriter:
    def __init__(self,filepath):
        self.__fh = open(filepath,"w")
        self.__write_webvtt_head()
 
    def __del__(self):
        self.__fh.close

    def __sec2timefmt(self,sec):
        h= int(sec / 3600)
        m= (sec % 3600)/60
        s= int(sec % 60)
        return '%02d:%02d:%02d' % (h,m,s)

    def __write_webvtt_head(self):
        self.__fh.write("WEBVTT\n")
        self.__fh.write("NOTE\n")
        self.__fh.write("\n")

    def write_webvtt_line (self,start_sec, end_sec, line):
        s="{0}.000 --> {1}.000\n{2}\n\n".format(
                        self.__sec2timefmt(start_sec),
                        self.__sec2timefmt(end_sec),
                        line
                        )
        print s 
        self.__fh.write(s)
        #self.__fh.write("{0}.000 --> {1}.000\n{2}\n\n".format(
        #                self.__sec2timefmt(start_sec),
        #                self.__sec2timefmt(end_sec),
        #                line
        #                )
        #            )
