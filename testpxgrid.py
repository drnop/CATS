#!/usr/bin/python3
import json
import sys
import os
import cats
import getopt
import traceback


helpmessage = '''Program to test CATS ISE PXGRID Interface.

Usage:

testpxgrid.py -h -d -c -s server -p <save password from previous registration> -j jsonfile  -n nodename -t textdescription of node  -o operation -i ip -m mac")

-h is for help (this text).
-d is for adding debug
-c is to force client cert auth (requires details in jsonfile)
-j is a json file for configuration details (required if certs are used)
-s allows to specify server (overriding what is in  json file)
-n nodename allows to specific nodename (overriding what is in json file)
-p password save password
-t textdescription of node
-o operation

This program tests and explains usage of CATS ISE PXGRID Interface.

ISE PXGRID can be accessed via
1. client cert auth, specified with -c option
2. password based auth (requires manual approval through ISE GUI)

1. Client Cert Auth

./testpxgrid.py -c  

..<output below, dumping the session table and more>
{
    "adNormalizedUser": "chris",
    "adUserDomainName": "labrats.se",
    "adUserNetBiosName": "LABRATS",
    "adUserResolvedDns": "CN=Christophe,OU=Users,OU=Admin,DC=labrats,DC=se",
    "adUserResolvedIdentities": "chsvenss@labrats.se",
    "auditSessionId": "ac106301000730005e1c7c89",
    "calledStationId": "194.16.1.242",
    "catsresult": "OK",
    "ctsSecurityGroup": "CiscoSEs",
    "endpointCheckResult": "none",
    "endpointProfile": "Macintosh-Workstation",
    "identitySourcePortEnd": 0,
    "identitySourcePortFirst": 0,
    "identitySourcePortStart": 0,
    "ipAddresses": [
        "10.1.201.72"
    ]
..<truncated>

Options for client cert can be specified in json file given by -j parameter. (default ./iseconfig.json).
Options include stuff for cert auth like location of certs and keys and passwords for private key.

{"ise_server":"100.120.120.38",
 "pxgrid_client_cert":"/home/hacke/pxGridCerts/drnop_.cer",
 "pxgrid_client_key":"/home/hacke/pxGridCerts/drnop_.key",
 "pxgrid_client_key_pw":"C1sco12345","pxgrid_server_cert":
 "/home/hacke/pxGridCerts/labrats-INFRA-AD02-CA_.cer",
 "pxgrid_nodename":"drnop"}

2. Password based auth

For password based auth, the only thing needed is the ISE server IP (-s option) anad the nodename specified with the -n options.
The password is then automatically generated and remembered by the script. (Requires manual approval in ISE GUI).

It is possible to specify the password with the -p option, but that should only be used if the node has already been registered to pxgrid
(maybe by previous run of script).

hacke@hackubuntu:/usr/lib/cgi-bin$ ./testpxgrid.py -n mickeymouse -s 100.120.120.38 -d
opening config file iseconfig.json
not cert auth
POST:   https://100.120.120.38:8910/pxgrid/control/AccountCreate
HEADERS:{'Content-Type': 'application/json', 'Accept': 'application/json'}
DATA:   {"nodeName": "mickeymouse"}
password is tMarvLrjdpSixsWo
Activation necessary!
POST:   https://100.120.120.38:8910/pxgrid/control/AccountActivate
HEADERS:{'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': ' Basic bWlja2V5bW91c2U6dE1hcnZMcmpkcFNpeHNXbw=='}
DATA:   {"description": ""}

2a. Here it is necessary to manually approve activation in ISE GUI (for certs, ISE can be configured for automatic approval.)

2b. Output truncated.

<...>
        {
            "acl": "permit ip",
            "description": "Permit IP SGACL",
            "generationId": "0",
            "id": "92951ac0-8c01-11e6-996c-525400b48521",
            "ipVersion": "IPV4",
            "name": "Permit IP"
        },
        {
            "acl": "permit ip log",
            "description": "Permit IP with logging",
            "generationId": "1",
            "id": "ca148250-f82c-11e6-bb16-0242a39eb2d7",
            "ipVersion": "IPV4",
            "name": "Permit_IP_Log"
        },
        {
            "acl": "deny icmp\ndeny ip",
            "description": "drop all",
            "generationId": "1",
            "id": "345a77f0-f9e5-11e6-bb16-0242a39eb2d7",
            "ipVersion": "IPV4",
            "name": "drop ./testpxgrid.py -n mickeymouse -s 100.120.120.38 -d -p  tMarvLrjdpSixsWo
"
        }
    ]
}
password used was tMarvLrjdpSixsWo

2c. Note the password presented in the last line. If you want to run another pxGrid session with the same pxnodename that has now been activated/approved, this password should be passed to the script. (No activation in ISE GUI is now necessary.

./testpxgrid.py -n mickeymouse -s 100.120.120.38 -d -p  tMarvLrjdpSixsWo


3. Operations performed after authentication (1 or 2).

Upon successful authentication and attachment to pxgrid bus, the program will try to perform an operation, specified by the -o option.

'''

OPERATIONS = [{'name':"getsessions",'description':"get sessions : -i ip or -m mac t only give session for one device"},
              {'name':"getbindings",'description':"get SXP bindings"},
              {'name':"getsecuritygroups",'description':"get TrustSec Security Group"},
              {'name':"getsecuritygroupacls",'description':"get TrustSec Security Group ACLs"},
              {'name':"getprofiles",'description':"get Profiles"},
              {'name':"getfailures",'description':"get RADIUS failures"}
              ]


def exception_info(err):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    estring = "{} {} {} {} {}".format(err,exc_type, fname, exc_tb.tb_lineno,traceback.format_exc())
    return estring

def print_help():
    print(helpmessage)
    for o in OPERATIONS:
        print("-o {} : Description {}".format(o["name"],o["description"]))
        
def main(argv):

    ISE_SERVER = ""
    ISE_PASSWORD = ""
    PXGRID_CLIENT_CERT = ""
    PXGRID_CLIENT_KEY = ""
    PXGRID_CLIENT_KEY_PASSWORD = ""
    PXGRID_SERVER_CERT = ""
    PXGRID_NODENAME = ""
    
    mac = ""
    ip  = ""
    debug = False
    password = ""
    nodename2 = ""
    certauth = False
    description = ""
    server2 = ""
    password2 = ""
    jsonfile = "iseconfig.json"
    operation = "getsessions"
    try:
        opts, args = getopt.getopt(argv,"hcdp:i:m:n:t:j:s:o:")
        for opt, arg in opts:
            if opt == '-h':
                print_help()
                sys.exit(2)
            if opt == ("-d"):
                debug = True
            if opt == ("-c"):
                certauth = True
            if opt == ("-i"):
                ip = arg
            if opt == ("-m"):
                mac = arg
            if opt == ("-n"):
                nodename2 = arg
            if opt == ("-t"):
                description = arg
            if opt == ("-j"):
                jsonfile = arg
            if opt == ("-s"):
                server2 = arg
            if opt == ("-p"):
                password = arg
            if opt == ("-o"):
                operation = arg
                found = False
                for o in OPERATIONS:
                    if operation == o["name"]:
                        found = True
                if not found:
                    raise ValueError
    except Exception as err:
        print("Error in syntax")
        print_help()
        sys.exit(2)

    try:

        try:
            print("opening config file {}".format(jsonfile))
            creds = json.loads(open(jsonfile).read())
            ISE_SERVER = creds["ise_server"]
            PXGRID_PASSWORD = creds["ise_password"]
            PXGRID_CLIENT_CERT = creds["pxgrid_client_cert"]
            PXGRID_CLIENT_KEY = creds["pxgrid_client_key"]
            PXGRID_CLIENT_KEY_PASSWORD = creds["pxgrid_client_key_pw"]
            PXGRID_SERVER_CERT = creds["pxgrid_server_cert"]
            PXGRID_NODENAME = creds["pxgrid_nodename"]
        except Exception as e:
            print("unable to open jsonfile {}, continuing (will only work for password based auth)".format(jsonfile))
                  
# override file config options for ise server and nodename        
        if server2:
            ISE_SERVER = server2
        if nodename2:
            PXGRID_NODENAME = nodename2

        if not ISE_SERVER:
            print("No ISE server specified, nor in file or with -s option")
            print_help()
            sys.exit(2)

        if certauth:
            if debug:
                print("NODE {} CLIENT CERT {} KEY {} SERVER CERT {}".format(PXGRID_NODENAME,PXGRID_CLIENT_CERT,PXGRID_CLIENT_KEY,PXGRID_SERVER_CERT))
            if PXGRID_NODENAME and PXGRID_CLIENT_CERT and PXGRID_CLIENT_KEY and PXGRID_CLIENT_KEY_PASSWORD and PXGRID_SERVER_CERT:
                  i = cats.ISE_PXGRID(server=ISE_SERVER,nodename=PXGRID_NODENAME,clientcert=PXGRID_CLIENT_CERT,clientkey=PXGRID_CLIENT_KEY,clientkeypassword=PXGRID_CLIENT_KEY_PASSWORD,servercert=PXGRID_SERVER_CERT,description=description,debug=debug,logfile="")
                  ## i.activate seems to be necessary once for the node name  for cert based auth

                  i.activate()
            else:
                  print("Not all options for cert auth specified in json file, see -h for help")
                  sys.exit(2)                  
        else:
            print("not cert auth")
            if PXGRID_NODENAME:
                  i = cats.ISE_PXGRID(server=ISE_SERVER,nodename=PXGRID_NODENAME,password=password,description=description,debug=debug,logfile="")
                  password = i.getPassword()                  
                  print("password is {}".format(password))                  
                  i.activate()
            else:
                  print("Nodename must be specified for password based auth, see -h for help")
                  sys.exit(2)                  
   
        if operation == "getsessions":
            rsp = i.getSessions(ip=ip,mac=mac)
        if operation == "getbindings":
            rsp = i.getBindings()
        if operation == "getsecuritygroups":            
            rsp = i.getSecurityGroups()
        if operation == "getsecuritygroupacls":                        
            rsp = i.getSecurityGroupACLs()
        if operation == "getprofiles":                        
            rsp = i.getProfiles()
        if operation == "getfailures":                        
            rsp = i.getFailures()
            
        print(json.dumps(rsp,indent=4,sort_keys=True))

        print("password used was {}".format(password))
        
    except Exception as err:
        print("ERROR")
        print(exception_info(err))
        print("ERROR")
        
if __name__ == "__main__":
    main(sys.argv[1:])

'''
1.   i = cats.ISE_PXGRID(nodename=nodename, password=password, client this client that)
    2a   saved_password = i.password()

< 2 may be bypassed >
2.     i.activateAccount(nodename)    <----- create ssl context, or get nodename password   , may be bypassed if already exists

<2 may be bypassed>

3.  i.getSessions

    

   

'''
