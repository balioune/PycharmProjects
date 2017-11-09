from __future__ import print_function
import sys
import libvirt


conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

caps = conn.getCapabilities() # caps will be a string of XML
stat = conn.getInfo()
domains=conn.listAllDomains()
#print('Capabilities:\n'+caps)
print('Listing all domains :\n')
for domain in domains:
    print (str(domain))

conn.close()
exit(0)

xml= "<domain type='qemu'> \
  <name>QEmu-fedora-i686</name> \
  <memory>219200</memory> \
  <currentMemory>219200</currentMemory> \
  <vcpu>2</vcpu> \
  <os> \
    <type arch='x86_64' machine='pc-i440fx-trusty'>hvm</type> \
    <boot dev='hd'/> \
  </os> \
  <features> \
    <acpi/> \
    <apic/> \
    <pae/> \
  </features> \
  <clock offset='utc'/> \
  <on_poweroff>destroy</on_poweroff> \
  <on_reboot>restart</on_reboot> \
  <on_crash>restart</on_crash> \
  <devices> \
    <emulator>/usr/bin/kvm-spice</emulator> \
    <disk type='file' device='disk'> \
      <driver name='qemu' type='qcow2'/> \
      <source file='/home/nfv/router.img'/> \
      <target dev='vda' bus='virtio'/> \
    </disk> \
    <disk type='file' device='disk'> \
      <driver name='qemu' type='raw'/> \
      <source file='/home/nfv/router.iso'/> \
      <target dev='vdb' bus='virtio'/> \
    </disk> \
    <interface type='network'> \
      <source network='default'/> \
    </interface> \
    <graphics type='vnc' port='-1'/> \
  </devices> \
</domain>"

