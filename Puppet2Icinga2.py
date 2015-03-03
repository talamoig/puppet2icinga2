import MySQLdb
import re
import subprocess

class Puppet2Icinga2:
   '''
   Class to generate Icinga configuration file from host in a puppet
   database (using the storeconfigs puppetmaster option)
   '''
   template="cms-host"
   hostheader="object Host \"%s\""
   addrline="address= \"%s\""
   match2hostgroup=[]
   servicehost=None

   ALLHOST_QUERY="select name,ip from hosts where ip is not NULL"
   FACTS_QUERY="select fact_names.name,value from fact_values,fact_names,hosts where host_id=hosts.id and hosts.name='%s' and fact_name_id=fact_names.id"

   execfile('config.py')

   def __init__(self):
      for regex in self.regex2hostgroup.keys():
         m=re.compile(regex)
         self.match2hostgroup.append((m,self.regex2hostgroup[regex]))

   def fromdb(self,query):
      db = MySQLdb.connect(self.dbhost,
                           self.dbuser,
                           self.dbpasswd,
                           self.dbname)
      cur = db.cursor()
      cur.execute(query)
      all=cur.fetchall()
      return all

   def get_hostgroup2host(self):
      if self.servicehost!=None:
         return self.servicehost
      self.servicehost={}
      for host,services in self.services().items():
         services.sort()
         servicekey=','.join(services)
         if not self.servicehost.has_key(servicekey):
            self.servicehost[servicekey]=[]
         self.servicehost[servicekey].append(host)

      hostgroups=[self.hostgroupname(x) for x in self.servicehost.values()]
      
      for service,hostlist in self.servicehost.items():
         name=self.hostgroupname(hostlist)
         if hostgroups.count(name)>1:
            index=0
            while self.servicehost.has_key('%s-%s'%(name,index)):
               index+=1
            name='%s-%s'%(name,index)
         self.servicehost[name]=self.servicehost.pop(service)
      return self.servicehost

   def host2hostgroup(self,hostname):
      for k,v in self.get_hostgroup2host().items():
         if hostname in v:
            return k
      return None

   def hostgroups(self):
      return self.get_hostgroup2host().keys()

   def services(self):
      '''
      Returns a dictionary where:
      -keys are hostnames
      -values is a list of services provided by the hostname of the
      key
      With "provide" we mean that the given service can be checked on
      the host with the NRPE protocol
      '''
      hosts=self.hosts()
      hostservices={}
      for host,_,_ in hosts:
         services=self.getnrpeservices(host)
         hostservices[host]=services   
      return hostservices

   def hosts(self):
      '''
      Returns a list of all the hosts.
      Each element is a triple with:
      -hostname
      -ip address
      -facts

      facts is a list of facter facts of the given host
      '''
      hosts=[]
      for row in self.fromdb(self.ALLHOST_QUERY):
         hostname=row[0]
         if hostname=='cmsrm-an008.roma1.infn.it':
            continue
         ip=row[1]
         facts=self.getfacts(hostname)
         hosts.append((hostname,ip,facts))
      return hosts
   
   def getclasses(self,hostname):
      classes=self.fromdb("select title from resources,hosts where restype='Class' and resources.host_id=hosts.id and hosts.name='%s'"%hostname)
      return [x[0] for x in classes]

   def getfacts(self,hostname):
      facts=self.fromdb(self.FACTS_QUERY%hostname)
      facts=filter(lambda (x,y):x not in self.ignorefacts,facts)
      return facts

   def hostgroupname(self,hostlist):
      name=hostlist[0]
      if len(hostlist)==1:
         return hostlist[0]      
      index=len(hostlist[0])
      while len(set(map(lambda x:x[:index],hostlist)))>1:
         index=index-1
      if index==0:
         return "hostgroup"
      return map(lambda x:x[:index],hostlist)[0]
         
   def definehost(self, hostname, ip, facts):
      hostgroup=self.host2hostgroup(hostname)
      hostgroupline="groups = [ \"%s\" ]"%hostgroup
      ret="%s{\n\timport \"%s\"\n\t%s\n\t%s\n\t%s\n}"%(self.hostheader%hostname,self.template,self.addrline%ip,hostgroupline,"\n\t".join(["vars."+fact+" = \""+val+"\"" for (fact,val) in facts]))
      return ret

   def defineservice(self,host,service):
      return "object Service \"%s\" {\n\thost_name = \"%s\"\n\tcheck_command = \"nrpe\"\n\tvars.nrpe_command = \"%s\"\n}"%(service,host,service)

   def definehostgroup(self,hostgroup):
      return 'object HostGroup "%s" {\ndisplay_name = "%s"\n}'%(hostgroup,hostgroup)

   def getnrpeservices(self,hostname):
      plugin_path="/usr/lib64/nagios/plugins/check_nrpe"
      output = subprocess.Popen([plugin_path, "-H", hostname, '-c', 'metanrpe'], stdout=subprocess.PIPE).communicate()[0]
      services=output.split("\n")
      servicename=re.compile("[a-zA-Z-_ ]")
      services=filter(lambda x: servicename.match(x),services)
      services=list(set(services))
      return services

              
