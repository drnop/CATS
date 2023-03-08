
import requests
import os
import sys
import json
import getopt
import cats


def print_help():
    print("running python " + str(sys.version_info))
    name = os.path.basename(__file__)
    print("Usage: " + name + " -d (for debug) -u username")
   

def main(argv):

     
  
    debug = False
    try:
        opts, args = getopt.getopt(argv,"du:")
        for opt, arg in opts:
            if opt == '-h':
                print_help()
                sys.exit(2)
            if opt == ("-d"):
                debug = True
            if opt == ("-u"):
                upn= arg
           
    except Exception as err:
        
        print_help()
        sys.exit(2)
    try:
        creds = json.loads(open("graphapi.json").read())
        tenant = creds["tenant"]
        client_id = creds["client_id"]
        client_secret = creds["client_secret"]      
    except Exception as e:
        print(str(e))
        print("Failed to open graphapi.json or file does not contain credentials")
        sys.exit(2)
   
    aad = cats.AAD(tenant=tenant,client_id=client_id,client_secret=client_secret,debug=debug)
    rsp = aad.getRoles()
    print(json.dumps(rsp,indent=4,sort_keys=True))
    rsp = aad.getGroupsAndRolesByUPN(upn)
    print(json.dumps(rsp,indent=4,sort_keys=True))
if __name__ == "__main__":
    main(sys.argv[1:])
