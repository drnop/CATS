#!/usr/bin/python3                                                                                                                         
import json
import sys
import requests
import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from time import gmtime,strftime
import datetime
import os
import getopt
import re
import cats



def print_help():
    print("running python " + str(sys.version_info))
    name = os.path.basename(__file__)
    print("Usage: " + name + " -o { get | post | delete | investigate | report } -n dnsname-i ip  -u url -d (for debug) -D days -H hours -M minutes")
    print("print -o post -n dnsname -u url  ## add dnsname to enforce")
    print("print -o delete -n dnsname -u url  ## delete dnsname to enforce")
    print("print -o get -n dnsname -u url  ## list dnsnames to enforce")
    print("print -o investigate -n dnsname -i ip  ## investigate dns name or ip")
    print("print -o report -n dnsname -i ip  -D days -H hours -M minutes ## report dns name")    
    
def main(argv):

    domain = ""
    ip = ""
    url = ""
    operation = "get"
    debug = False
    days = 0
    hours = 1
    minutes = 0
    try:
        opts, args = getopt.getopt(argv,"dho:n:u:i:D:H:M:")
        for opt, arg in opts:
            if opt == '-h':
                print_help()
                sys.exit(2)
            if opt == ("-d"):
                debug = True
            if opt == ("-o"):
                operation = arg
            if opt == ("-n"):
                domain = arg
            if opt == ("-u"):
                url = arg
            if opt == ("-i"):
                ip = arg
            if opt == ("-D"):
                days = int(arg)
            if opt == ("-H"):
                hours = int(arg)
            if opt == ("-M"):
                minutes = int(arg)
                
    except Exception as err:
        
        print_help()
        sys.exit(2)

    try:
        creds = json.loads(open("orbital.json").read())
        CLIENT_ID = creds["client_id"]
        CLIENT_PASSWORD = creds["client_password"]
            
    except Exception as e:
        print(str(e))
        print("Failed to open orbital.json")
        print("Ensure you have defined API_xxx stuff in the script for the script to work")
    if debug:
        print("Using ID{}".format(CLIENT_ID))        
        print("Using PASSWORD {}".format(CLIENT_PASSWORD))        

    o = cats.ORBITAL(client_id=CLIENT_ID,client_password=CLIENT_PASSWORD,debug=debug)
    o.get_token()
    dum = ""
    rsp = o.query(dum,dum)
    print("id is " + rsp["ID"])
    print("link is " + "https://orbital.amp.cisco.com/jobs/" + rsp["ID"] + "/results")
#    rsp = o.results()
#    print(json.dumps(rsp,indent=4,sort_keys=True))
    
    

            

if __name__ == "__main__":
    main(sys.argv[1:])
