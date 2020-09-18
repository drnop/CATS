#!/usr/bin/python3

from datetime import date, timedelta
import datetime
import json
import time
import cats
import getopt
import sys

def print_help():
    print("running python " + str(sys.version_info))
    name = os.path.basename(__file__)
    print("Usage: " + name + " -h -f filename(with json creds) -d debug -u username")



def main(argv):
    
    api_ikey="xxxxxxxxxxx"
    api_skey="yyyyyyyyyyy"
    duo_host="api-12345.duosecurity.com"
    username="user1"
    debug = False
    filename = "duoadmin.json"
    status = "active"
    try:
        opts, args = getopt.getopt(argv,"hdu:f:s:")
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

        

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit(2)
        if opt == ("-u"):
            username = arg
        if opt == '-d':
            debug = True
        if opt == "-s":
            status  = arg
        if opt == '-f':
            filename = arg

    try:
        creds = json.loads(open(filename).read())
        api_ikey = creds["api_ikey"]    
        api_skey = creds["api_skey"]    
        duo_host = creds["duo_host"]
        
    except Exception as e:
        print(str(e))
        print("Failed to open/parse {}".format(filename))
            
            
    duo1=cats.DUO_ADMIN(api_ikey=api_ikey,api_skey =api_skey, duo_host=duo_host, debug=debug, logfile="")
    r=duo1.users(username=username)
    id1= r["response"][0]["user_id"]
    print("user id is " + id1)

    r = duo1.modify_user(id1,status=status)
    print(json.dumps(r,indent=4,sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1:])


