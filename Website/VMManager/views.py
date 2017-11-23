from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import VirtualMachine

import xml.etree.ElementTree as ET
import uuid
import libvirt
import os

# Create your views here.
def index(request):
    # createNewVM("Name", 2, 500000, 30)
    return HttpResponse("VMManager works")

def createNewVM(request, name, cores, ram, storage):
    if not request.user.is_authenticated():
        return

    vm = VirtualMachine()

    vm.Name = name
    vm.VMID = uuid.uuid4()
    vm.CPUCores = cores
    vm.RAMAmount = ram
    vm.DISKSize = storage

    vm.save()

    os.system(
        "sudo qemu-img create -f qcow2 /Users/john/Documents/vm_images/{NAME}.qcow2 {SIZE}G".format(
            NAME = vm.Name,
            SIZE = vm.DISKSize
        )
    )

    os.system(
        "qemu-img resize /Users/john/Documents/vm_images/{NAME}.qcow2 +{SIZE}G".format(
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
    imagepath = '/home/jurrewolff/Desktop/images/disk.img'
    imagepath = imagepath.replace('disk', str(nameroot.text))
    root2[1][1].set('file', str(imagepath))

    # Change iso file (This one is the right way)
    isopath = '/home/jurrewolff/Desktop/iso/linuxmint-18.2-cinnamon-64bit.iso' # LET OP! OS MOET NOG IN DE FORM WORDEN GEVRAAGD! VERVANG DAN LINUXMINT NAAR 'os'!
    isopath = isopath.replace('os', str(os))
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
    conn.createXML(xmlstr)
    

    return ""

def destroyVM(name):
    
    return ""
