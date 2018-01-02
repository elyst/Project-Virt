from __future__ import print_function

import sys
import xml.etree.ElementTree as ET
import uuid
import libvirt
import os
import time
import random, string
import pathlib

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .models import VirtualMachine



# Create your views here.
def index(request):
    return HttpResponse("VMManager works")

@login_required
def createNewVM(request, name, cores, ram, storage, os_choice):
    
    #Initialise VM model
    vm = VirtualMachine()
    
    #Save VM information
    vm.Name = name.replace(" ", "-")
    vm.User = request.user
    vm.VMID = uuid.uuid4()
    vm.CPUCores = cores
    vm.RAMAmount = ram
    vm.DISKSize = storage
    vm.SSH_User = generateRandChar(5)
    
    #Check for duplicate names in Database
    if duplicates('Name', vm.Name, 1) != True:
        messages.error(request, 'A Virtual Machine with this name already exists')
        return False

    #Check if user reached maximum amount of ram
    if maximum(str(request.user), ram) != True:
        messages.error(request, 'You have reached the maximum amount of Virtual Machines')
        return False
        
    os.system(
        "sudo qemu-img create -f qcow2 /home/jurrewolff/Desktop/images/{NAME}.qcow2 {SIZE}G".format(
            NAME = vm.Name,
            SIZE = vm.DISKSize
        )
    )

    os.system(
        "qemu-img resize /home/jurrewolff/Desktop/images/{NAME}.qcow2 +{SIZE}G".format(
            NAME = vm.Name,
            SIZE = vm.DISKSize
        )
    )

    # XML file to parse
    xml = 'vmTemplate.xml'

    # Parse XML file
    tree = ET.parse(str(xml))
    root = tree.getroot()

    # Indexing of all necessary parents
    root2 = tree.find('devices')
    root3 = root2.find('interface')
    root4 = root3.find('source')

    # Change VM name
    nameroot = tree.find('name')
    nameroot.text = str(vm.Name)

    # Change uuid
    uniqueid = uuid.uuid4()                 # Generate random uuid
    uuidroot = tree.find('uuid')
    uuidroot.text = str(uniqueid)

    # Change mem size
    mroot = tree.find('memory')
    mroot.text = str(ram)
    mroot2 = tree.find('currentMemory')
    mroot2.text = str(ram)

    # Change number of vcpu's
    vcpuroot = tree.find('vcpu') #Tree.find has to be used here bcause there's no parent?
    vcpuroot.text = str(cores)

    # Change disk image name accordingly
    imagepath = '/home/jurrewolff/Desktop/images/disk.qcow2'
    imagepath = imagepath.replace('disk', str(nameroot.text))
    root2[1][1].set('file', str(imagepath))

    # Change iso file (This one is the right way)
    isopath = os_choice # LET OP! OS MOET NOG IN DE FORM WORDEN GEVRAAGD! VERVANG DAN LINUXMINT NAAR 'os'!
    isopath = isopath.replace('os', str(os_choice))
    root2[2][1].set('file', str(isopath))

    # Change value of network interface
    root4.set('bridge', 'virbr0')           # Bridges have to be automized!

    # Write changes to XML file
    tree.write('vmTemplate.xml')

    # Reparse for updated file 
    tree = ET.parse(str(xml))
    root = tree.getroot()

    # Convert the bytestream 'root' to workable string
    xmlbyte = ET.tostring(root, encoding="us-ascii", method="xml")
    xmlstr = xmlbyte.decode()

    # Send the string to libvirt
    conn = libvirt.open()
    conn.defineXML(xmlstr)

    #Create new SSH user
    newSshUser(request, VMIP(vm.Name), vm.SSH_User)

    #If everything ok, save VM
    vm.save() 

    messages.success(request, 'Your VM has been created. \n An email with your credentials has been send!')
    return True

def duplicates(field, name, counter):
    field = field + '__iexact'

    #PYLINT REGISTERS AN ERROR OVER HERE. JUST IGNORE THAT, IT IS NO ERROR
    data = VirtualMachine.objects.filter(**{ field: name })
    count = 0
    for each in data:
        count += 1
    
    if count >= counter:
        return False
    return True

def maximum(user, ram):
    #PYLINT REGISTERS AN ERROR OVER HERE. JUST IGNORE THAT, IT IS NO ERROR
    data = VirtualMachine.objects.filter(User__exact=user)
    count = 0
    test = []
    for each in data:
        count += each.RAMAmount
    count = count + ram
    if count > 8000000:
        return False    
    return True

def start(name):
    # Setup connection to hypervisor
    conn = libvirt.open('qemu:///system')

    dom0 = conn.lookupByName(name)
    dom0.create()
    print(dom0.state())

def stop(name):
    conn = libvirt.open('qemu:///system')

    dom0 = conn.lookupByName(name)
    dom0.destroy()
    print(dom0.state())
    
def reboot(name):
    conn = libvirt.open('qemu:///system')

    dom0 = conn.lookupByName(name)
    dom0.shutdown()
    time.sleep(2)

    dom0.start()  

def suspend(name):
    conn = libvirt.open('qemu:///system')

    dom0 = conn.lookupByName(name)
    dom0.suspend()
    print(dom0.state())

def deleteVM(name):
    conn = libvirt.open('qemu:///system')
    dom0 = conn.lookupByName(name)

    if dom0.state() == [1, 1]:
        dom0.destroy()
    
    dom0.undefine() # Erases vm from existence (Atleast from kvm's perspective)
    os.remove('/home/jurrewolff/Desktop/images/{NAME}.qcow2'.format(NAME = name)) # Removes disk
    
    instance = VirtualMachine.objects.get(Name = name)
    instance.delete()   # Deleted entry from database

def VMstate(user):
    conn = libvirt.open('qemu:///system')

    # Iterates through names of users vms ?creates tuple inside of a list?
    data = VirtualMachine.objects.filter(User__exact=user)
    vmlist = 0

    for value in data:
        dom0 = conn.lookupByName(value.Name)
        print(dom0.state())
        if dom0.state() == [1, 1]:
            value.State = 'Running'
            print(value.State)
            value.save()
        elif dom0.state() == [5, 0] or [5, 2]:
            value.State = 'Shut down'
            print(value.State)
            value.save()
        elif dom0.state() == [3, 1]:
            print(value.State)
            value.State = 'Suspended'
            value.save()

def VMIP(VMname):
    ip_list = []
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system', file=sys.stderr)
        exit(1)

    domainName = VMname
    dom = conn.lookupByName(domainName)
    if dom == None:
        print('Failed to get the domain object', file=sys.stderr)

    ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)

    print("The interface IP addresses:")
    for (name, val) in ifaces.iteritems():
        if val['addrs']:
            for ipaddr in val['addrs']:
                if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                    ip_list.append(ipaddr['addr'])
                    print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4")
                elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
                    ip_list.append(ipaddr['addr'])
                    print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV6")

    conn.close()
    return ip_list

#Send email with credentials when vm is created
def sendMail(request, ssh_user, temp_password):
    current_user = str(request.user)
    data = User.objects.filter(username__exact=current_user)
    for value in data:
        user_email = value.email

    body = '{} \n {} \n'.format(ssh_user, temp_password)    
    email = EmailMessage('Credentials VMX Virtual Machine', body, to=[user_email])
    email.send()
      
#Generate a random set of chars
def generateRandChar(amount):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(amount))

#Create new sshUser for specific VM
def newSshUser(request, DomainIp, SSHuser):
    
    #Initialise new user
    NewUser = SSHuser
    NewPassword = generateRandChar(8)
    GoPath = os.getenv('GOPATH')

    #Create user directory
    path = '/{}/src/github.com/tg123/sshpiper/sshpiperd/example/workingdir/{}'.format(GoPath, NewUser)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    #Create ssh connection credentials
    f= open("{}/sshpiper_upstream".format(path),"w+")
    f.write("root@{}:22".format(DomainIp))
    f.close()

    sendMail(request, NewUser, NewPassword)
