#!/bin/env python
from optparse import OptionParser
from Puppet2Icinga2 import Puppet2Icinga2

hostgroup_file="hostgroup_file"
service_file="service_file"
host_file="host_file"

parser = OptionParser()

parser.add_option("-o", "--host", dest=host_file,
                  help="write hosts definitions to FILE", metavar="FILE")
parser.add_option("-s", "--service", dest=service_file,
                  help="write service definitions to FILE", metavar="FILE")
parser.add_option("-g", "--hostgroup", dest=hostgroup_file,
                  help="write hostgroups definitions to FILE", metavar="FILE")

(options, args) = parser.parse_args()


p2i=Puppet2Icinga2()

if options.host_file:
   hosts=p2i.hosts()
   for hostname,ip,facts in hosts:   
      print p2i.definehost(hostname, ip, facts)

if options.service_file:
   services=p2i.services()
   for hostname in services.keys():
      for service in services[hostname]:
         print p2i.defineservice(hostname,service)

if options.hostgroup_file:
   hostgroups=p2i.hostgroups()
   for h in hostgroups:
      print p2i.definehostgroup(h)
