from django.shortcuts import render, HttpResponse
from .models import VirtualMachine

import uuid
import libvirt
import os

# Create your views here.
def index(request):
    # createNewVM("Name", 2, 500000, 30)
    return HttpResponse("VMManager works")

def createNewVM(name, cores, ram, storage):
    vm = VirtualMachine()

    vm.Name = name
    vm.VMID = uuid.uuid4()
    vm.CPUCores = cores
    vm.RAMAmount = ram
    vm.DISKSize = storage

    vm.save()

    os.system(
        "sudo qemu-img create -f qcow2 /home/niels/EXTDrive/VM/{NAME}.qcow2 {SIZE}G".format(
            NAME = vm.Name,
            SIZE = vm.DISKSize
        )
    )

    os.system(
        "qemu-img resize /home/niels/EXTDrive/VM/{NAME}.qcow2 +{SIZE}G".format(
            NAME = vm.Name,
            SIZE = vm.DISKSize
        )
    )

    vmTemplate = """<domain type='kvm'>
                        <name>{NAME}</name>
                        <uuid>{UUID}</uuid>
                        <memory>{MEMORY}</memory>
                        <currentMemory>{MEMORY}</currentMemory>
                        <vcpu>{CPU}</vcpu>
                        <os>
                            <type>hvm</type>
                            <boot dev='cdrom'/>
                        </os>
                        <features>
                            <acpi/>
                        </features>
                        <clock offset='utc'/>
                        <on_poweroff>destroy</on_poweroff>
                        <on_reboot>restart</on_reboot>
                        <on_crash>destroy</on_crash>
                        <devices>
                            <emulator>/usr/bin/kvm</emulator>
                            <disk type="file" device="disk">
                                <driver name="qemu" type="qcow2"/>
                                <source file="/home/niels/EXTDrive/VM/{NAME}.qcow2"/>
                                <target dev="vda" bus="virtio"/>
                                <address type="pci" domain="0x0000" bus="0x00" slot="0x04" function="0x0"/>
                                </disk>
                            <disk type="file" device="cdrom">
                                <driver name="qemu" type="raw"/>
                                <source file="/home/niels/Downloads/ubuntu.iso"/>
                                <target dev="hdc" bus="ide"/>
                                <readonly/>
                                <address type="drive" controller="0" bus="1" target="0" unit="0"/>
                            </disk>
                            <interface type='bridge'>
                            <source bridge='virbr0'/>
                            <mac address="00:00:00:00:00:00"/>
                            </interface>
                            <controller type="ide" index="0">
                            <address type="pci" domain="0x0000" bus="0x00" slot="0x01" function="0x1"/>
                            </controller>
                            <input type='mouse' bus='ps2'/>
                            <graphics type='vnc' port='-1' autoport="yes" listen='0.0.0.0'/>
                            <console type='pty'>
                            <target port='0'/>
                            </console>
                        </devices>
                        </domain>""".format(
                            NAME = vm.Name,
                            MEMORY = vm.RAMAmount,
                            CPU = vm.CPUCores,
                            UUID = vm.VMID
                        )
    
    conn = libvirt.open()
    conn.createXML(vmTemplate)
    

    return ""