# Import Elementtree(ET) --> ET is used for reading and editing xml files
import xml.etree.ElementTree as ET
import uuid

# XML file to parse
xml = 'kvm.xml'

# Variables from form
name = 'NoSQL'
ram = '524288'                           # In Kilobytes
cores = '2.5'
os = 'ubuntu'                               # Has to match the names that are in the iso folder!

# Parse XML file
tree = ET.parse(str(xml))

# Indexing of all necessary parents
root2 = tree.find('devices')
root3 = root2.find('interface')
root4 = root3.find('source')

# Change VM name
nameroot = tree.find('name')
nameroot.text = name

# Change uuid
uuid = uuid.uuid4()                         # Generate random uuid
uuidroot = tree.find('uuid')
uuidroot.text = str(uuid)

# Change mem size
mroot = tree.find('memory')
mroot.text = memory
mroot2 = tree.find('currentMemory')
mroot2.text = ram

# Change number of vcpu's
vcpuroot = tree.find('vcpu')                # Tree.find has to be used here bcause there's no parent? 
vcpuroot.text = cores

# Change disk image name accordingly
imagepath = '/home/jurrewolff/Desktop/git/Project-Virt/kvm/images/disk.img'
imagepath = imagepath.replace('disk', str(nameroot.text))
root2[1][1].set('file', str(imagepath))

# Change iso file (This one is the right way)
isopath = '/home/jurrewolff/Desktop/git/Project-Virt/kvm/iso/os.iso'
isopath = isopath.replace('os', str(os))
root2[2][1].set('file', str(isopath))

# Change value of network interface
root4.set('bridge', 'br0')                  # Bridges have to be automized!

# Write changes to XML file
tree.write('kvm.xml')