#!/usr/bin/python
import random
import subprocess
import sys
import os

''' SETUP NEW HOST SERVER
Look at installing this https://pypi.python.org/pypi/py-cpuinfo/0.1.0
and http://cagewebdev.com/index.php/raspberry-pi-showing-some-system-info-with-a-python-script/


Use puppet to manage the ntpd to remote configure the time servers
Yum does not configure the .conf files for the service, but is great for installation

SERVICES
1. MLOCATE
1. NTPD
2. KVM/QEM
3. OPENSTACK
4. VNC SERVER
yum groupinstall Desktop
5. YUM UPDATE
puppet module install puppetlabs-openstack
puppet module install arusso-vnc
$vnc_arusso = {
  'user' => 'arusso',
  'args' => '-SecurityTypes=VeNCrypt,TLSPlain -PlainUsers=arusso pam_service=login',
}
$vnc_brusso = {
  'user' => 'brusso',
  'args' => '-SecurityTypes=VeNCrypt,TLSVNC',
}

class { 'vnc': servers => [ $vnc_arusso, $vnc_brusso ] }

 yum groupinstall Desktop
 
'''


service_yum_list=["puppet", "mlocate", "kvm", "vnc-server", "qemu-kvm", "python-virtinst", 
"virt-manager", "virt-top", "virt-viewer", "libvirt", "libvirt-client"]
service_yum_group_list=["Desktop", "GNOME Desktop", "Graphical Administration Tools"]
service_puppet_list=["puppetlabs-ntp", "puppetlabs-openstack"]

# For Centos 7
#ln -sf /lib/systemd/system/runlevel5.target /etc/systemd/system/default.target


# Ensure client has IP of master
action = "echo "+"'"+'10.0.0.1    masterpup.local.org'+"'"+" >>/etc/hosts"
subprocess.call(action, shell=True)

subprocess.call("rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-7.noarch.rpm", shell=True)
#subprocess.call("rpm -ivh http://yum.puppetlabs.com/puppetlabs-release-el-6.noarch.rpm", shell=True)
#subprocess.call("cd /etc/yum.repos.d;wget http://masterpup.local.org/files/puppetlabs.repo", shell=True)
print ("\n" * 2)
print "yum clean all"
print ("\n" * 2)

subprocess.call("yum clean all", shell=True)


def getYUMservices(categ, argv) :
  total=''
  items=len(argv)

  for y in argv:
     items -= 1
	 
     if items == 0 :
        total += y 
     else :
        total += y + ' '
		
     if (categ == 'g') :
        action = 'yum groupinstall -y ' + total
     else :
        action = 'yum install -y ' + total

  print ("\n" * 2)
  print action
  print ("\n" * 2)
  
  return action
  
def setservices(argv) :

  for y in argv :
	action = "service "+y+" restart"
	print (action)
	subprocess.call(action, stderr=open('/dev/null', 'w'), shell=True)

	action = "chkconfig "+y+" on"
	print (action)
	subprocess.call(action, stderr=open('/dev/null', 'w'), shell=True)
	
  return 

def installPUPPETmodules(argv) :
  i = 0
  
  for y in argv :
    action = 'puppet module install ' + argv[i]
    i += 1
    print action
    print "\n" 
    subprocess.call(action, shell=True)

  return 
   
print "Services to YUM install: "
subprocess.call( getYUMservices('', service_yum_list), shell=True)
print '\n'

#https://www.youtube.com/watch?v=61X2Armexf8
#Research updated config from module
#subprocess.call("cd /etc/puppet;wget http://masterpup.local.org/files/puppet.conf", shell=True)
subprocess.call("service puppet restart", shell=True)
subprocess.call("chkconfig puppet on", shell=True)

#ON SERVER SIDE
# CRON JOB TO SIGN ALL CERTS
#puppet cert sign --all


print "Services to YUM Group install: "
subprocess.call( getYUMservices('g', service_yum_group_list), shell=True)
print ("\n" * 2)

print "Services to PUPPET install: "
installPUPPETmodules(service_puppet_list)
print ("\n" * 2)

print "Starting services..."
setservices(service_yum_list)
setservices(service_yum_group_list)
print ("\n" * 2)

#Update all packages
subprocess.call("yum -y update", shell=True)
subprocess.call("reboot", shell=True)







