#/usr/bin/env python

#Importing neccessary modules
import subprocess
import random
import optparse
import termcolor2
import colorama
import re

colorama.init()
possibitities = ['A','B','C','D','E','F','1','2','3','4','5','6','7','8','9','0']
 
#Function to generate random MAC Address
def getNewMAC():
   
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
    except:
        print(termcolor2.colored(("[!!] *Something went wrong! Quiting the progrm..."),'red'))
        exit(0)
              
        
    
#Getting arguments entered by the user 
def getArguments():
    #Creating parser object
    parser = optparse.OptionParser()

    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC address")
    parser.add_option("-m","--mac",dest="macAddress",help="New MAC address Eg. --resMAC FA:22:33:44:AD:22")
    parser.add_option("-r","--random",dest="randomMAC",action="store_true", help="Assign random MAC Address")  
    
    (options,arguments) = parser.parse_args()
    
    #Checking if the user enter interface name or not
    if not options.interface:
        print(termcolor2.colored(("[!!] *Interface name required! Use '--help' for more info."),'red'))
        exit(0)
        
    if(options.randomMAC and not(options.macAddress)):
        if(not(type(options.randomMAC)== int) and (not(options.randomMAC in [0,1]))):
            print(termcolor2.colored(("Invalid Arguments!!! Use '--help' for more info."),'red'))
            exit(0)
    elif(not(options.randomMAC) and (options.macAddress)):
        mac = options.macAddress
        test = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",mac).group(0)
   
        if(str(test)!=mac):
            print(termcolor2.colored(("Invalid MAC Address!"),'red'))
            exit(0)
        else:
            for i in test:
                if (i in possibitities) or (i==':'):
                    continue
                else:
                    print(termcolor2.colored(("Invalid MAC Address!"),'red'))
                    exit(0)
                    
    else:
        print(termcolor2.colored(("Can't use -m and -r together! Use '--help' for more info."), 'red'))
        exit(0)
           
    return options

def checkResult(interface,trueMAC):
    results = subprocess.check_output(["ifconfig ",interface])
    resMAC = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",results)
    if(resMAC):
        if resMAC == trueMAC:
            return True
    else:
        return False        
    

#Getting arguments entered by user
options = getArguments()

interface = options.interface

#Getting new MAC Address if user does not specify MAC Address
try:
    newMACAddress = options.newMACAddress
except:
    print(termcolor2.colored(("[+] *Configuring a random MAC Address to the interface..."),'yellow'))
    newMACAddress = getNewMAC()


changeMACAddress(interface,newMACAddress)
status = checkResult(interface,newMACAddress)

if(status):
    print(termcolor2.colored(("[+] *MAC Address changed successfully..."),'green'))
else:
    print(termcolor2.colored(("[+] *Unable to change MAC Address!!!"),'red'))
    

