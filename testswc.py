#!/usr/bin/python3


import json
import sys
import pprint
import time
import os
import getopt
import re
import cats


operations = [
    "getalerts",
    "getauditlogs",
    "getobservations",
    "getroles",
    "getflows"
    ]

def print_help():
    print("running python " + str(sys.version_info))
    name = os.path.basename(__file__)
    print("Usage: " + name + " -h -o operation -D days -H hours - M minutes -d debug -n Hostname -g guid -i internal_ip -e external_\
ip ")
    print(".. where operation is ")
    for o in operations:
        print(".. -o {}".format(o))
    
def main(argv):

    debug = False
    days = 1
    hours = 1
    minutes = 1    
    operation = ""
    swcid = ""
    username = ""
    try:
        opts, args = getopt.getopt(argv,"hdD:o:H:n:i:e:s:M:u:")
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit(2)
        if opt == ("-o"):
            operation = arg
            found = False
            for op in operations:
                if operation == op:
                    found = True
                    break
            if not found:
                print("Invalid -o option")
                print_help()
                sys.exit(2)
        if opt == ("-u"):
            username = arg
        if opt == '-d':
            debug = True
        if opt == ("-D"):
            days = int(arg)
        if opt == ("-H"):
            hours = int(arg)
        if opt == ("-M"):
            minutes = int(arg)
        if opt == ("-i"):
            internal_ip = arg
        if opt == ("-e"):
            external_ip = arg
        if opt == ("-n"):
            hostname = arg
        if opt == ("-s"):
            swcid = arg

    if not operation:
        print("-o not specified")
        print_help()
        sys.exit(2)
    try:
        creds = json.loads(open("swcapi.json").read())
        BASEURL = creds["baseurl"]    
        API_USERNAME = creds["api_username"]    
        API_KEY = creds["api_key"]

    except Exception as e:
        print(str(e))
        print("Failed to open swcapi.json")
        print("Ensure you have defined API_KEY in the script for the script to work")
    if debug:
        print("Using BASEURL {} API USERNAME {} and API KEY {}".format(BASEURL,API_USERNAME,API_KEY))
    swc = cats.SWC(baseurl=BASEURL,username=API_USERNAME,api_key=API_KEY,debug=debug,logfile="")

    if (operation == "getalerts"):    
        rsp = swc.getAlerts(swcid=swcid)
    if (operation == "getauditlogs"):    
        rsp = swc.getAuditLogs(swcid=swcid,username=username)
    if (operation == "getobservations"):
        rsp = swc.getObservations(swcid=swcid)
    if (operation == "getroles"):
        rsp = swc.getRoles(swcid=swcid)
    if (operation == "getflows"):
        rsp = swc.getFlows()
        
    print(json.dumps(rsp,indent=4,sort_keys=True))
    
if __name__ == "__main__":
    main(sys.argv[1:])
