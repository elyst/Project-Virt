import sys
import xml.etree.ElementTree as ET
import uuid
import libvirt
import os
import random, string
import pathlib
import after_response
import shutil
from time import time, sleep

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
    vm.SSH_User = generateUser(5)
    
    #Check for duplicate names in Database
    if duplicates('Name', vm.Name, 1) != True:
        messages.error(request, 'A Virtual Machine with this name already exists')
        return False

    #Check if user reached maximum amount of ram
    if maximum(str(request.user), ram) != True:
        messages.error(request, 'You have reached the maximum amount of Virtual Machines')
        return False


    #If everything ok, save VM
    vm.save()
    
    os.system('qemu-img create -f qcow2 -b /home/john/Desktop/base_images/{}.qcow2 /home/john/Desktop/images/{}.qcow2'.format(os_choice, name))

    os.system(
        "sudo qemu-img resize /home/john/Desktop/images/{NAME}.qcow2 +{SIZE}G".format(
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
    imagepath = '/home/john/Desktop/images/disk.qcow2'
    imagepath = imagepath.replace('disk', str(nameroot.text))
    root2[1][1].set('file', str(imagepath))

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
    
    #Start VM
    start(vm.Name)
    
    #Gaining async ip while function returned success
    VMIP.after_response(request, vm.Name)

    messages.success(request, 'Your VM has been created. \n An email with your credentials will be send shortly!')
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
    stop(name)
    sleep(2)
    start(name)
      
def suspend(name):
    conn = libvirt.open('qemu:///system')

    dom0 = conn.lookupByName(name)
    dom0.suspend()
    print(dom0.state())

def deleteVM(name):
    data = VirtualMachine.objects.filter(Name__exact = name)
    go_path = os.environ.get('GOPATH')
    for value in data:
        ssh_user = value.SSH_User
    
    shutil.rmtree('{}/src/github.com/tg123/sshpiper/sshpiperd/example/workingdir/{}'.format(go_path, ssh_user))    
    conn = libvirt.open('qemu:///system')
    dom0 = conn.lookupByName(name)

    if dom0.state() == [1, 1]:
        dom0.destroy()
    
    dom0.undefine() # Erases vm from existence (Atleast from kvm's perspective)
    os.remove('/home/john/Desktop/images/{NAME}.qcow2'.format(NAME = name)) # Removes disk
    
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

@after_response.enable
def VMIP(request, VMname):
    ip_command = 'for mac in `virsh domiflist {} |grep -o -E "([0-9a-f]{{2}}:){{5}}([0-9a-f]{{2}})"` ; do arp -e |grep $mac  |grep -o -P "^\d{{1,3}}\.\d{{1,3}}\.\d{{1,3}}\.\d{{1,3}}" ; done'.format(VMname)
    result = ""
    count = 0
    while result == "":
        if count >= 40:
            print('failed to get the ip from {}'.format(VMname))
            break
        result = os.popen(ip_command).read()
        if result != "":
            result = result.replace("\n", "")
            print('successfully got ip from {} as {}...'.format(VMname, result))
        else:    
            print('Waiting for ip response of {}...'.format(VMname))
        sleep(5)
        count += 1

    data = VirtualMachine.objects.filter(Name__exact = VMname)
    for value in data:
        SSH_User = value.SSH_User 
    newSshUser(request, result, SSH_User, VMname)

#Send email with credentials when vm is created
def sendMail(request, ssh_user, temp_password, ssh_credentials):
    current_user = str(request.user)
    data = User.objects.filter(username__exact=current_user)
    for value in data:
        user_email = value.email

    body = 'ssh username: {} \n root/ssh password: {} \n login like this: {}'.format(ssh_user, temp_password, ssh_credentials)    
    email = EmailMessage('Credentials VMX Virtual Machine', body, to=[user_email])
    email.send()
      
#Generate a random set of chars
def generateRandChar(amount):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(amount))


#Create new sshUser for specific VM
def newSshUser(request, DomainIp, SSHuser, VMname):
    
    #stop vm
    stop(VMname)

    #Initialise new user
    NewUser = SSHuser
    NewPassword = changeRootPassword(generateRandChar(8), VMname)
    count = 0
    while NewPassword == None:
        if count >= 40:
            print('It took too long.. sawry bro')
            break
        else:
            print('Waiting for new root password...')
            sleep(5)
            count += 1

        
    GoPath = os.getenv('GOPATH')

    #Create user directory
    path = '/{}/src/github.com/tg123/sshpiper/sshpiperd/example/workingdir/{}'.format(GoPath, NewUser)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    os.system('chmod 755 /{}/src/github.com/tg123/sshpiper/sshpiperd/example/workingdir/{}'.format(GoPath,NewUser))

    #Create ssh connection credentials
    f= open("{}/sshpiper_upstream".format(path),"w+")
    f.write("root@{}:22".format(DomainIp))
    f.close()
    os.system('chmod 400 /{}/src/github.com/tg123/sshpiper/sshpiperd/example/workingdir/{}/sshpiper_upstream'.format(GoPath,NewUser))

    ssh_credentials = "ssh {}@127.0.0.1 -p 2222".format(SSHuser)
    
    sendMail(request, NewUser, NewPassword, ssh_credentials)

    #spin up vm!
    start(VMname)



def generateUser(length):
    Alphabet= 'abcdefghijklmnopqrstuvwxyz'
    username = ''
    count = 0
    while count != length:
        letter = random.choice(Alphabet)
        username = username + letter
        count += 1

    return username


def changeRootPassword(password, VMname):
   
    #Write password to temporary file
    f= open("/tmp/secret","w+")
    f.write(password)
    f.close()
    
    #change root password
    os.system('sudo virt-sysprep --password root:file:/tmp/secret -a /home/john/Desktop/images/{}.qcow2'.format(VMname))
    
    #sleep for a while zzzz..
    sleep(10)

    #delete temp password
    os.system('sudo rm /tmp/secret')
    print('Successfully changed root password!')
    return password



    
    
        

  
