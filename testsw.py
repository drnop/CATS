#!/usr/bin/python3                                                                                                                         
import json
import sys
import requests
import pprint
from time import gmtime,strftime
from datetime import datetime,timedelta
import time
import os
import getopt
import re
import ipaddress
import cats
## define structure for simple gets (atomic structure)


OPERATIONS = [
    {"id": "secevents",      "help":"-d -D -H -M -e" },
    {"id": "getflows",       "help":"--sIP <subject IP> --ptag <peer HostGroup> " },
    {"id": "getcognitive",   "help":"--sIP <IP>" },
    {"id": "gethostgroups",  "help":"--sIP <IP>" },   
    {"id": "eventlist",  "help":""} 
]

def commit_suicide(err):
    print("Exception! {}\n ".format(str(err)))
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    sys.exit(2)


def print_help():
    print("running python " + str(sys.version_info))
    name = os.path.basename(__file__)
    print("Usage: " + name + " -s server -u username -p password -o operation --sip <subject ip> --pip <peer ip> -D days -H hours -M minutes -d ")
    
    print("-D Days and -H hours -M minutes back in time to search")
    print("-d adds debugging")
    for o in OPERATIONS:
        print("operation can be: ")
        print("-o " + o["id"] + " # " + o["help"])
    
    sys.exit()
def main(argv):

    server = "1.1.1.1"
    username = "admin"
    password = "insertyourown"
    tag = ""
    debug = False
    sourceip = ""
    targetip   = ""
    days = 0
    hours = 1
    minutes = 1    
    wait = 3
    operation = "secevents"
    eventids = []
    try:
        opts, args = getopt.getopt(argv,'-hds:u:p:o:D:H:M:e:',['sip=','ptag='])
        for opt, arg in opts:
            if opt == '-h':
                print_help()
            if opt == ("-s"):
                server = arg
            if opt == ("-u"):
                username = arg
            if opt == ("-p"):
                password = arg
            if opt == ("-o"):
                operation = arg
                found = False
                for o in OPERATIONS:
                    if o["id"] == operation:
                        found = True
                if not found:
                    print_help()
                    sys.exit()
            if opt == ('-D'):
                days = int(arg)
            if opt == ("-M"):
                minutes = int(arg)
            if opt == ("-H"):
                hours = int(arg)
            if opt == ("-e"):
               eventid = int(arg)
               eventids.append(eventid)
            if opt == ("-d"):
                debug = True
            if opt == ("--sip"):
                subjectip = arg
                try:
                    ipaddress.ip_address(subjectip)
                except:
                    print("--sip subjectip is not a valid IP: {}".format(subjectip))
                    print_help()
                    sys.exit()
            if opt == ("--pip"):
                targetip = arg
                try:
                    ipaddress.ip_address(targetip)
                except:
                    print("--pip peerip is not a valid IP: {}".format(targetip))
                    print_help()
                    sys.exit()

    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    
        
    sw = cats.SW(server,username,password,debug=debug,logfile="")

    if operation == "getflows":
        rsp = sw.getFlows([subjectip])
        print(json.dumps(rsp,indent=4,sort_keys=True))
    if operation == "gethostgroups":
        rsp = sw.getHostGroups()
        print(json.dumps(rsp,indent=4,sort_keys=True))
    if operation == "getcognitive":
        rsp = sw.getCognitiveIncidents(ip=subjectip)
        print(json.dumps(rsp,indent=4,sort_keys=True))
    if operation == "secevents":
        rsp = sw.searchSecurityEvents(days=0,hours=0,minutes=2,seceventids=eventids)
        print(json.dumps(rsp,indent=4,sort_keys=True))  
    if operation == "eventlist":
        rsp = sw.eventList()
        print(json.dumps(rsp,indent=4,sort_keys=True))                
        '''
        time.sleep(30)
        rsp = sw.searchSecurityEvents(days=0,hours=0,minutes=2)
        print(json.dumps(rsp,indent=4,sort_keys=True))                
        time.sleep(30)
        rsp = sw.searchSecurityEvents(days=0,hours=0,minutes=2)        
        print(json.dumps(rsp,indent=4,sort_keys=True))                
        '''
    sys.exit()
    



    

if __name__ == "__main__":
    main(sys.argv[1:])
