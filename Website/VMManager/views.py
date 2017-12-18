from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

from .models import VirtualMachine
import xml.etree.ElementTree as ET
import uuid
import libvirt
import os
import time

# Create your views here.
def index(request):
    # createNewVM("Name", 2, 500000, 30)
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
    
    #Check for duplicate names in Database
    if duplicates('Name', name, 1) != True:
        messages.error(request, 'A Virtual Machine with this name already exists')
        return False

    #Check if user reached maximum amount of ram
    if maximum(str(request.user), ram) != True:
        messages.error(request, 'You have reached the maximum amount of Virtual Machines')
        return False

    #If everything ok, save VM
    vm.save() 
        
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
    nameroot.text = str(name)

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
    vcpuroot = tree.find('vcpu')            # Tree.find has to be used here bcause there's no parent? 
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



    messages.success(request, 'Your VM has been created.')
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
    userIterator = VirtualMachine.objects.values('Name') # Iterates through names of users vms ?creates tuple inside of a list?
    vmlist = 0

    print(userIterator)

    for VMname in userIterator:
        if VMname.state() == [1, 1]:
            VMname.State = 'Running'
            VMname.save()
        elif VMname.state == [5, 2]:
            VMname.State == 'Shut down'
            VMname.save
        elif VMname.state() == [3, 1]:
            VMname.State == 'Suspended'
            VMname.save()