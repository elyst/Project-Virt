# Import Elementtree(ET) --> ET is used for reading and editing xml files
import xml.etree.ElementTree as ET

# Parse XML file
tree = ET.parse('kvm.xml')

# Find desired tag to edit
root = tree.find('devices')
root2 = root.find('interface')
root3 = root2.find('source')

# Change mem size
memroot1 = tree.find('memory')
memroot1.text = '1024'
memroot2 = tree.find('currentMemory')
memroot2.text = '1024'

# Change number of vcpu's
vcpuroot = tree.find('vcpu')
vcpuroot.text = '2'

# Change iso file
isoroot = root.find('')

# Change value of network interface
alter = root3.set('bridge', 'br0')

# Write changes to XML file
tree.write('kvm.xml')