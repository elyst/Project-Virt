import os
import libvirt
import libvirt_qemu
import xml.etree.ElementTree as ET


class VirtualManager():
    def __init__(self, diskpath, baseimagepath):
        self.diskpath = diskpath
        self.baseimagepath = baseimagepath

    def createVM(self, vm):
        # Code to create VM

        try: 
            # Create disk
            os.system(
                'qemu-img create -f qcow2 -b {}/{}.qcow2 {}/{}.qcow2'.format(self.baseimagepath, vm.os, self.diskpath, vm.name)
            )
        except:
            return False

        # Create VM
        try:
            f = open("vmTemplate.xml")
            parseXML = ET.parse(f)
            f.close()

            r = parseXML.getroot()
            r.find("name").text = vm.name
            r.find("uuid").text = vm.uuid
            r.find("memory").text = str(vm.memory)
            r.find("currentMemory").text = str(vm.memory)
            r.find("vcpu").text = str(vm.cores)
            print (self.diskpath + vm.name)
            r.find("./devices/disk/source").set("file", self.diskpath + "/" + vm.name + ".qcow2")

            conn = libvirt.open("qemu:///system")
            conn.defineXML(
                ET.tostring(r).decode()
            )

        except Exception as e:
            print ("Something went wrong", e)

        return True
    
    def rebootVM(self, vm):
        # Code to reboot VM
        return

    def shutdownVM(self, vm):
        # Shutdown VM
        return
    
    def startVM(self, vm):
        # Start VM
        return

    def destroyVM(self, vm):
        # Destroy VM
        return