#/usr/bin/env python

#Importing neccessary modules
import subprocess
import random
import optparse
import termcolor2
import colorama

colorama.init()

#Function to generate random MAC Address
def getNewMAC():
    possibitities = ['A','B','C','D','E','F','1','2','3','4','5','6','7','8','9','0']
    mac = []

    #Creating random MAC Address
    for i in range(1,13):
        unit = random.choice(possibitities)
        mac.append(unit)
        if ((i%2 == 0) and not(i==12)):
            mac.append(':')
    
    return ''.join(mac)   

 
#Function to change MAC Address
def changeMACAddress(interface,newMACAddress):
    print(termcolor2.colored(("[+] *Changing MAC Address for "+ interface + " to new adress "+ newMACAddress ),'yellow'))
    
    try:
        subprocess.call(["ifconfig",interface," down"])
        subprocess.call(["ifconfig",interface," hw"," ether ",newMACAddress])
        subprocess.call(["ifconfig",interface," up",])
        return True
    except:
        return False
  
def getArguments():
    #Creating parser object
    parser = optparse.OptionParser()

    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC address")
    parser.add_option("-m","--mac",dest="macAddress",help="New MAC address")

    (options,arguments) = parser.parse_args()
    
    #Checking if the user enter interface name or not
    if not options.interface:
        print(termcolor2.colored(("[!!] *Interface name required! Use '--help' for more info."),'red'))
        exit(0)
 
    return options


#Getting arguments entered by user
options = getArguments()

interface = options.interface

#Getting new MAC Address if user does not specify MAC Address
try:
    newMACAddress = options.newMACAddress
except:
    print(termcolor2.colored(("[+] *Configuring a random MAC Address to the interface..."),'yellow'))
    newMACAddress = getNewMAC()


status = changeMACAddress(interface,newMACAddress)

if(status):
    print(termcolor2.colored(("[+] *MAC Address changed successfully..."),'green'))
else:
    print(termcolor2.colored(("[+] *Unable to change MAC Address!!!"),'red'))
    

