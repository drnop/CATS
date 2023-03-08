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

##### secrets and orgids used for the different APIs
API_ORGID = "insertyourown"
API_ENFORCE_TOKEN = "insertyourown"
API_INVESTIGATE_TOKEN = "insertyourown"
API_KEY = "insertyourown"
API_SECRET = "insertyourown"

def print_help():
    print("running python " + str(sys.version_info))
    name = os.path.basename(__file__)
    print("Usage: " + name + "-x <identity> -S start -P stop") 
    
def main(argv):

    domains = ""
    ip = ""
    url = ""
    operation = "get"
    debug = False
    start = "-1days"
    stop = "now"
  
    identity = ""
    id_category = ""
    identity_string = ""
    category_string = ""
    try:
        opts, args = getopt.getopt(argv,"dho:n:u:i:S:P:x:c:")
        for opt, arg in opts:
            if opt == '-h':
                print_help()
                sys.exit(2)
            if opt == ("-d"):
                debug = True
            if opt == ("-o"):
                operation = arg
            if opt == ("-n"):
                domains = arg
            if opt == ("-u"):
                url = arg
            if opt == ("-i"):
                ip = arg
            if opt == ("-P"):
                stop = arg
            if opt == ("-S"):
                start = arg
            if opt == ("-x"):
                identity_string = arg
            if opt == "-c":
                category_string = arg
           
                
    except Exception as err:
        
        print_help()
        sys.exit(2)

    try:
        creds = json.loads(open("umbrella.json").read())
        API_KEY = creds["api-key"]        
        API_SECRET = creds["api-secret"]        
    except Exception as e:
        print(str(e))
        print("Failed to open umbrellaapi.json")
        print("Ensure you have defined API_xxx stuff in the script for the script to work")
    if debug:
        print("Using API KEY {}".format(API_KEY))        
        print("Using API SECRET {}".format(API_SECRET))        

    u = cats.UMBRELLA2(key=API_KEY,secret=API_SECRET,debug=debug)
    #rsp = u.admin_users()
    #print(json.dumps(rsp,indent=4,sort_keys=True))
    #sys.exit(2)
    rsp = u.identities()
    print("Retrieved Identities")
    data = rsp["data"]
    if identity_string:
        for d in data:
            print(d["label"])
            if d["label"] == identity_string:
                identity = str(d["id"])
           

    rsp = u.categories()
    print("Retrieved Categories")
    data = rsp["data"]
    for d in data:
        print(d["label"])
        if d["label"] == category_string:
            id_category = d["id"]
       
    print("identity is "+str(identity))
    print("id_newly_seen_domain " + str(id_category))
  

    

    rsp = u.reports_activity_dns(start=start,stop=stop,ip=ip,identityids=identity,categories=id_category,domains=domains)
    print(json.dumps(rsp,indent=4,sort_keys=True))

    sys.exit(2)
   
            

if __name__ == "__main__":
    main(sys.argv[1:])
