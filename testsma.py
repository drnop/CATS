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
    "reportDLP",
    "reportDLPpolicy",
    "getobservations",
    "getroles",
    "getflows"
    ]

apis = [
    "mail_dlp_outgoing_policy_detail",
    "mail_dlp_outgoing_policy_detail/dlp_action_delivered",
    "mail_dlp_outgoing_policy_detail/dlp_action_dropped",
    "mail_dlp_outgoing_policy_detail/dlp_action_encrypted",
    "mail_dlp_outgoing_policy_detail/dlp_incidents_critical",
    "mail_dlp_outgoing_policy_detail/dlp_incidents_high",
    "mail_dlp_outgoing_policy_detail/dlp_incidents_low",
    "mail_dlp_outgoing_policy_detail/dlp_incidents_medium",            
    "mail_dlp_outgoing_policy_detail/total_dlp_incidents",
    "mail_dlp_outgoing_traffic_summary",
    "mail_dlp_outgoing_traffic_summary/dlp_incidents_critical",
    "mail_dlp_outgoing_traffic_summary/dlp_incidents_high",
    "mail_dlp_outgoing_traffic_summary/dlp_incidents_low",
    "mail_dlp_outgoing_traffic_summary/dlp_incidents_medium",
    "mail_dlp_outgoing_traffic_summary/total_dlp_incidents",
    "mail_dlp_users_policy_detail",
    "mail_dlp_users_policy_detail/outgoing_dlp_action_delivered",
    "mail_dlp_users_policy_detail/outgoing_dlp_action_dropped",
    "mail_dlp_users_policy_detail/outgoing_dlp_action_encrypted",
    "mail_dlp_users_policy_detail/outgoing_dlp_action_quarantined",
    "mail_dlp_users_policy_detail/outgoing_dlp_incidents_critical",
    "mail_dlp_users_policy_detail/outgoing_dlp_incidents_high",
    "mail_dlp_users_policy_detail/outgoing_dlp_incidents_medium",
    "mail_dlp_users_policy_detail/outgoing_dlp_incidents_low",
    "mail_dlp_users_policy_detail/total_dlp_incidents",
    "mail_dmarc_incoming_traffic_summary",
    "mail_authentication_incoming_domain",    
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
    days = "1"
    hours = "1"
    minutes = "1"    
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
            days = arg
        if opt == ("-H"):
            hours = arg
        if opt == ("-M"):
            minutes = arg
        if opt == ("-i"):
            internal_ip = arg
        if opt == ("-e"):
            external_ip = arg
        if opt == ("-n"):
            hostname = arg
        if opt == ("-s"):
            swcid = arg

    try:
        creds = json.loads(open("smaapi.json").read())
        SERVER = creds["server"]    
        USERNAME = creds["username"]    
        PASSWORD = creds["password"]
        PORT     = creds["port"]
        
    except Exception as e:
        print(str(e))
        print("Failed to open smaapi.json")
    if debug:
        print("Using SERVER {} USERNAME {} and PASSWORd {} PORT {}".format(SERVER,USERNAME,PASSWORD,PORT))
    sma = cats.SMA(server=SERVER,username=USERNAME,password=PASSWORD,port=PORT,debug=debug,logfile="")

    if (operation == "reportDLP"):    
        rsp = sma.reportDLPsummary(days=days)
    if (operation == "reportDLPpolicy"):    
        rsp = sma.reportDLPpolicy(days=days)


    
    if not operation:
        for api in apis:
            rsp = sma.report(api,days=days)
            print(json.dumps(rsp,indent=4,sort_keys=True))

    else:
        print(json.dumps(rsp,indent=4,sort_keys=True))            
if __name__ == "__main__":
    main(sys.argv[1:])
