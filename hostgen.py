#!/usr/bin/python                                                                                                                                               import MySQLdb                                                                                                                                                  import re

class2hostgroup={"Workernode::Emi3":"worker nodes"}
regex2hostgroup={"cmsrm-wn":"worker nodes"}
hostgroups={}
hostgroups["testgroup"]="cmsrm-test"

allhosts="select name,ip from hosts where ip is not NULL"                                                                                                                                                                                                                                                                       def fromdb(query):                                                                                                                                                 db = MySQLdb.connect(host="localhost", # your host, usually localhost                                                                                                                user="puppet", # your username                                                                                                                                  passwd="teppup", # your password
                        db="puppet") # name of the data base
   cur = db.cursor()
   cur.execute(query)
   return cur.fetchall()
                                                                                                                                                                def hostclasses(hostname):                                                                                                                                         classes=fromdb("select title from resources,hosts where restype='Class' and resources.host_id=hosts.id and hosts.name='%s'"%hostname)
   return classes


def definehost(hostname,ip):
   return "object Host \"%s\" {\n\timport \"cms-host\"\n\taddress=\"%s\"\n}"%(hostname,ip)                                                                                                                                                                                                                                                                                                                                                                                                      # print all the first cell of all the rows                                                                                                                      for row in fromdb(allhosts) :                                                                                                                                       hostname=row[0]                                                                                                                                                 ip=row[1]
    print definehost(hostname,ip)
    print hostclasses(hostname)

#    definehost(hostname,ip)
