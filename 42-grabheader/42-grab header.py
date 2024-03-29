__author__     = "J. Rappard"
__copyright__  = "Copyright 2023, J. Rappard"
__credits__    = ["Me", "Myself", "I"]
__license__    = "GNU General Public License v3.0"
__version__    = "0.3.1"
__maintainer__ = "J. Rappard"
__email__      = "python@rappard.eu"
__status__     = "Foo"

import sys
import requests
import socket
import json

#set variables
debug = False
showheader = "yes"
req = "bogus" 
line = 100
#debug = True

# Check parameters
if len(sys.argv) < 2:
    n = len(sys.argv[0])

    print("\n*****************************" + "*"*n)
    print("**               " + " "*n + "          **")
    print("**  Usage: " + sys.argv[0]+" <url> [-nh]   **")
    print("**               " + " "*n + "          **")
    print("*****************************" + "*"*n)
    
    sys.exit(2)

if sys.argv[1] == "-nh":
    print("\nMissing URL parameter. Do not use -nh as first parameter!")
    n = len(sys.argv[0])
    print("\n*****************************" + "*"*n)
    print("**               " + " "*n + "          **")
    print("**  Missing URL parameter. Do not use -nh as first parameter!"+ " "*(n-34) + "**")
    print("**  Usage: " + sys.argv[0]+" <url> [-nh]    **")
    print("**               " + " "*n + "          **")
    print("*****************************" + "*"*n)
    sys.exit(2)
    sys.exit()

try:
    if sys.argv[2] == "-nh":
        showheader = "no"
except:
        showheader = "yes"


#main
print("-"*line)
print("\n                    Getting your info for: " + sys.argv[1] + "\n")
print("-"*line)
try:
    gethostby_4 = socket.gethostbyname(sys.argv[1]) # get the IPv4 address
except:
    print("      Cannot fetch IPv4 address -  pyinfo: F01")

try:
    gethostby_6 = socket.AddressInfo(sys.argv[1], None, socket.AF_INET6) # get the IPv6 address
except Exception as e:
    print("        Cannot fetch IPv6 address -  info: F02")
    if debug == True:
        print(e)

try:
    req80 = requests.get("http://" + sys.argv[1], timeout=2) #do the request
    req = req80
except Exception as e:
    print(" Cannot request page over port 80 - error: F03")
    if debug == True:
        print(e)


try:
    req443 = requests.get("https://" + sys.argv[1], timeout=2) #do the request
    req = req443
except Exception as e:
    print("Cannot request page over port 443 - error: F03")
    if debug == True:
        print(e)

try:
    req_2 = requests.get("https://ipinfo.io/"+ gethostby_4+"/json") #get IP info
    resp_ = json.loads(req_2.text) #transform IP info
except:
    #print("Cannot get IP-info - error: F04")
    sys.exit("               Cannot get IP-info - error: F04" + "\n")
    print("-"*line)
    sys.exit()

# see if IP is bogon
try:
    if resp_["bogon"]:
        ip = "bogon"
        resp_["org"] = "Internal network - bogon address"
        resp_["loc"] = "n/a"
        resp_["region"] = "n/a"
        resp_["city"] = "n/a"
        resp_["country"] = "n/a"
except:
    #print("Regular IP address")
    ip = "routable"
finally:
    #all set
    bogoncheck = "ok"
    

#print(req)
print("-"*line)
print("\n                           Requested host: " + sys.argv[1])
print("                               IP address: " + gethostby_4)
print("                        Autonomous System: " + resp_["org"])
print("                                 Location: " + resp_["loc"])
print("                                   Region: " + resp_["region"])
print("                                     City: " + resp_["city"])
print("                                  Country: "+resp_["country"])
if req == "bogus":
    print("\n                              HTTP Status: Could not be retrieved")
else:
    print("\n                              HTTP Status: " + str(req.status_code) + "\n")

if showheader == "yes":
    try:
        print("-"*line)
        print("                              Headers for: " + sys.argv[1])
        rqhdr = str(req.headers)
        # Format the header info to human readable stuff
        # Block 1
        rqhdr = rqhdr.replace("{'","") # remove header
        rqhdr = rqhdr.replace("'}","") # remove trailer
        rqhdr = rqhdr.replace( "',","\n\n")
        rqhdr = rqhdr.replace("': '",": ")
        rqhdr = rqhdr.replace(" '","")
        rqhdr = rqhdr.replace(": ",":\n   ")
        rqhdr = rqhdr.replace("; ","\n   ")
        print(rqhdr)
        #hdr = json.loads(req.headers)
    except:
        print("Cannot connect to site. No site or header info available at this time.\n")
