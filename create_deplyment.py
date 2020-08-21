#this file is work inprogress 
#here for reference only 


import VzCloudCompute
import string, random, datetime, time, hmac, hashlib, base64, requests, json, getpass, sys
from termcolor import colored, cprint

def buildVdiskMounts(disks):
	vdiskItems = []
	for i, item in enumerate(disks):
		print item
		vdiskMnt = {}
		#ignore if neither templateHref nor diskHref are defined
		##if 'templateHref' not in item.keys() and 'diskHref' not in item.keys():
		##	continue
		#check disks for index, if not assign next
		##if 'index' in item.keys():
		##	vdiskMnt['index'] = item['index']
		##else:
		vdiskMnt['index'] = i
		if 'templateHref' in item.keys():
			vdiskMnt['vdisk'] = { 'fromVdiskTemplate': { 'href': item['templateHref'] }}
		if 'diskHref' in item.keys():
			vdiskMnt['vdisk'] = {'href': item['diskHref']}
			#hack in diskOps
		vdiskMnt['diskOps'] = IOps
		#append this vDisk to a list
		vdiskItems.append(vdiskMnt)
	print i
	print "buildVdiskMounts called"
	#return the list as the 'items' attribute
	return { 'items': vdiskItems }

def buildVnics(vnics):
	vnicItems = []

	for i, item in enumerate(vnics):
		vnic = {}
		print "item"
		print item
		print "vnicssss"
		print vnics
		print "vnic"
		print vnic

		#if 'publicIPHref' not in item.keys() and 'vnetHref' not in item.keys():
		#	continue

		#if 'index' in item.keys():
			#vnic['number'] = item['index']
		#else:
			#vnic['number'] = i
		#if 'publicIPHref' in item.keys():
		vnic['publicIpv4'] = { 'href': item['publicIPHref'] } ### TAB
		#if 'vnetHref' in item.keys():
			#vnic['vnet'] = { 'href': item['vnetHref'] }
		vnic['bandwidth'] = BandWidth
		vnic['number'] = 1
		vnicItems.append(vnic)
		print i
		print "buildVnics called"
		print json.dumps(vnic, indent=1 , sort_keys=True )
	return { 'items': vnicItems }

def GetFreePublicIP():
	freeIP = r.request('POST','/api/compute/ip-address')
	jobhref = freeIP['target']['href']
	youriphref = r.request('GET', jobhref)
	return youriphref

def SetFirewallRules(youriphref):
	firewall_content_type = 'application/vnd.terremark.ecloud.firewall-rule.v1+json'
	networkBoundaryInterfaceshref =  youriphref['networkBoundaryInterfaces']['href']
	networkBoundaryInterfacesjob = r.request('GET', networkBoundaryInterfaceshref)
	networkBoundary = networkBoundaryInterfacesjob['items'][0]['href']
	networkBoundaryjob = r.request('GET',networkBoundary)
	networkBoundaryhref = networkBoundaryjob['networkBoundary']['href']
	firewallrules = r.request('GET', networkBoundaryhref)
	firewallruleshref = firewallrules['firewallRules']['href']

	payload = {}
	payload['type'] = firewall_content_type
	r.request('PUT', firewallruleshref, payload)
	return


def DelRsrc(vmhref) :
	DelRsrcJob = r.request('DELETE', vmhref) #, printJSON=True)
	return DelRsrcJob

def DelVm(vmhref) :
	DelVmJob = r.request('DELETE', vmhref) #, printJSON=True)
	return DelVmJob


def DelSecDisk(diskhref) :
	DelSecDiskJob = r.request('DELETE', diskhref)#, printJSON=True)
	print DelSecDiskJob
	return DelSecDiskJob


def WaitOnRefCmpl(href ) :
	while (1) :
		#print href
		test = r.request('GET',href['href'])
		#print test
		if test['status']  == "COMPLETE":
			print "Done wait on href :", href
			break


def VmOff(vmhref) :  #not yet working
	offRef = r.request('GET', vmhref)

	r.request('POST', offRef['controllers']['powerOff']['href'])#, printJSON=True)     # power off the vm
	##print offRef
	#r.request('POST', , printJSON=True)     # power off the vm
	return


def FindOSTemplate(Template) :
	vdisktemplates = r.request('GET','/api/compute/vdisk-template')
	mytemplates = [x for x in vdisktemplates['items']]
	#find the one I need
	for x in range(len(mytemplates)):
			#print 	mytemplates[x]['description']
			if  mytemplates[x]['description'] == Template :
				keep = x
	Vdiskhref = mytemplates[keep]['href']
	#Vdiskhdesc = mytemplates[keep]['description']
	print json.dumps(Vdiskhref, indent=1 , sort_keys=True )
	return Vdiskhref


def FindHwVmTemplate(VmConfig) :
	all_templates = r.request('GET', '/api/compute/vm-template/' )
	template_names = [x for x in all_templates['items']]
	#find the one I need
	for x in range(len(template_names)):
			if  template_names[x]['description'] == VmConfig :
				keep = x
	VmTemplatehref = template_names[keep]['href']
	#VmTemplatehdesc = template_names[keep]['description']# selected_vm_template
	print json.dumps(VmTemplatehref, indent=1 , sort_keys=True )
	return VmTemplatehref


def MkDisk(DisdkName, DiskSize) :
	ExtrDiskSpec = {}
	ExtrDiskSpec['name'] = DisdkName
	ExtrDiskSpec['size'] = DiskSize
	ExtrDiskSpecjob = r.request('POST','/api/compute/vdisk', data=ExtrDiskSpec)
	return ExtrDiskSpecjob


def MkDiskRootMnt(iops, index) :
	vdiskMnt = {}
	vdiskMnt['diskOps'] = iops
	vdiskMnt['index'] = index
	vdiskMnt['vdisk'] = { 'fromVdiskTemplate': { 'href': Vdiskhref }}
	return vdiskMnt

def MkDiskMnt(iops, index) :
	vdiskMnt = {}
	vdiskMnt['diskOps'] = iops
	vdiskMnt['index'] = index
	vdiskMnt['vdisk'] = {'href': ExtrDisks[0]} ### take a look  !!!!
	return vdiskMnt


def MkPublicNic (bandwith, number , yourIP ) :
	vnic = {}
	vnic['publicIpv4'] = { 'href': yourIP['href'] }
	vnic['bandwidth'] = bandwith
	vnic['number'] = number
	return vnic


#############################
chassis_url = "https://amsa4.cloud.verizon.com"
accessKey = "XXXXXX"
secretKey = "XXXXXXXXXXX"
Template = "Turnkey Linux Core 13.0version 5 moded tempate  ...."
VmConfig = "8 VPU's 28 GB"
VMname = "MyVm_Using_REST_API"
IOps = 4000
BandWidth = 400
Cores = 7
Clock = 2000
Memory = 7168
Tag = "MyTag"
DiskAddName = "ExtraDiscTTT"
DiskAddSize = 2 *1024 #GBytes
#############################

#Create an instance of the VzREST class in variable 'r'
r = VzCloudCompute.VzREST(secretKey=secretKey, accessKey=accessKey,url=chassis_url)
print r._secretKey
print r._accessKey

data = {}

Vdiskhref = FindOSTemplate(Template)
#print json.dumps(Vdiskhdesc, indent=1 , sort_keys=True )

VmTemplatehref = FindHwVmTemplate(VmConfig)
#print json.dumps(VmTemplatehdesc, indent=1 , sort_keys=True )

ExtrDiskSpecJOB = MkDisk(DiskAddName, DiskAddSize)
#print json.dumps(ExtrDiskSpecJOB, indent=1 , sort_keys=True )
ExtrDiskSpecHref = ExtrDiskSpecJOB['target']['href']

ExtrDisks = []
ExtrDisks.append(ExtrDiskSpecHref)
#print json.dumps(ExtrDisks, indent=1 , sort_keys=True )

vdiskMnt = MkDiskRootMnt (IOps, 0)
vdiskMnt1 = MkDiskMnt (IOps, 1)
###vdiskMnt2 = MkDiskMnt (IOps, 2, disks )


vdiskItems = []
vdiskItems.append(vdiskMnt)
vdiskItems.append(vdiskMnt1)
####vdiskItems.append(vdiskMnt2)

data['vdiskMounts'] = {'items': vdiskItems }
print json.dumps(data['vdiskMounts'], indent=1 , sort_keys=True )

print "Public Net get IP"

yourIP = GetFreePublicIP()
SetFirewallRules(yourIP)
print "You allocated the address : ", yourIP['address'], '\n'

vnic = MkPublicNic (BandWidth, 0, yourIP)
vnicItems = []
vnicItems.append(vnic)
#print json.dumps(vnicItems, indent=1 , sort_keys=True )


data['vnics'] = {'items': vnicItems }

#set it up manually
VmTemplatehref = ""
data['processorCores'] = Cores
data['memory'] = Memory
data['processorSpeed'] = Clock

# from VmTemplatehref  - >> data['fromVmTemplate'] = { 'href': VmTemplatehref }

#--------------------------------------------------------------------------
data['name'] = VMname

#create VM
VmCreate = r.request('POST', '/api/compute/vm', data=data ) #, printJSON=True)
print "VmCreate"
print json.dumps(VmCreate, indent=1 , sort_keys=True )
VmHref = VmCreate['target']['href']
print VmHref

WaitOnRefCmpl(DelRsrc(VmHref))

userC = raw_input('enter the key to delete  disk')

while (1) :
	test = DelRsrc(ExtrDiskSpecHref)
	if test['description'] == "Error" :   #check for error
		print "Disk ERROR - repeat "
		continue
	WaitOnRefCmpl(test)
	break

while (1) :
	test = DelRsrc(yourIP['href'])
	if test['description'] == "Error" :   #check for error
		print "IP ERROR - repeat "
		continue
	WaitOnRefCmpl(test)
	break

#WaitOnRefCmpl(DelSecDisk (extra_diskHref))

print "end of the script reached -  success !!!"






