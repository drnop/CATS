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
    
## Admin API
    api_ikey="xxxxxxxxxxx"
    api_skey="yyyyyyyyyyy"
    duo_host="zzzzzzzzz"
    username="user1"
    debug = False
    filename = "duoadmin.json"
    
    try:
        opts, args = getopt.getopt(argv,"hdu:f:")
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

    print('** Users request for this user:', username)

    r=duo1.users(username=username)

    id1= r["response"][0]["user_id"]

    print("Users request's response:")
    print(json.dumps(r,indent=4,sort_keys=True))

    print('** logs for this user_id:', id1)

    today=str(date.today())

    yesterday1 = str(date.today() - timedelta(days=0))
    yesterday2 = str(date.today() - timedelta(days=4))
    print( "Time:",yesterday2, yesterday1)

    mintime=int(time.mktime(datetime.datetime.strptime(yesterday2, "%Y-%m-%d").timetuple())*1000)
    maxtime=int(time.mktime(datetime.datetime.strptime(yesterday1, "%Y-%m-%d").timetuple())*1000)
    response=duo1.logs(mintime=mintime, maxtime=maxtime, users=id1)
    print("response:",json.dumps(response,indent=4,sort_keys=True))

if __name__ == "__main__":
    main(sys.argv[1:])


