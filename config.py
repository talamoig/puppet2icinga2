dbhost="localhost"
dbuser="puppet"
dbpasswd="teppup"
dbname="puppet"

##class2hostgroup={"Workernode::Emi3":"worker nodes"}
regex2hostgroup={"cmsrm-wn":"worker nodes", "cmsrm-an":"analysis nodes", "cmsrm-st":"storage pools"}
class2hostgroup={}
host2hostgroup={}
ignorefacts=["sshdsakey","sshrsakey","sshfp_rsa","sshfp_dsa","processor0","processor1","processor2","processor3","processor4","processor5","processor6","processor7","processor8","processor9","processor10","processor11","processor12","macaddress_eth0","macaddress_eth1","network_eth0","network_eth1","lsbrelease","uptime_seconds","clientcert","boardserialnumber","serialnumber","rubysitedir","memorysize","macaddress","swapfree_mb","memorytotal","swapsize","ipaddress_eth0","ipaddress_eth1",'--- !ruby/sym "_timestamp"',"ipaddress","uuid","uptime_days","processorcount","memoryfree","uptime","uniqueid","swapfree"]
templatename="cms-host"
templatehost='template Host "cms-host" {\n\tmax_check_attempts = 5\n\tcheck_interval = 1m\n\tretry_interval = 30s\n\t\n\tcheck_command = "hostalive"\n}'
