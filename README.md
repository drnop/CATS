# CATS
Cisco API Tools for Security
... beta version

cats.py :  Collection of classes interacting with Cisco Security APIs.

The objective is to encapsulate complexities and differences across different APIs, to make it easy to write code without knowing
details about each APIs, how it authenticates, time formats etc.

## Example 1

As an example the follwoing code would give you the ISE session info for IP 10.1.33.33 without having to care about the logic attaching to pxGrid bus.

import cats
i=cats.ISE_PXGRID(server=SERVER,nodename=NODENAME,clientcert=CLIENT_CERT,clientkey=CLIENT_KEY,clientkeypassword=CLIENT_KEY_PASSWORD,servercert=SERVER_CERT,description=description,debug=debug,logfile="")
i.activate()
rsp = i.getSessions(ip=“10.1.33.33”)

## Example 2

Another example, to retrieve all IP flows from last hour for IP 10.1.33.33, without having to care about authenticating to Cisco Secure Network Analytics (tokens put in cookie + XSRF token, and without having to care about time formats or implement a while loop to accumulate events:

import cats
username = ...
password = ...
sourceip = "10.1.33.33"
days = 0
hours = 1
sw = cats.SW(server,username,password,debug=debug,logfile="")
rsp = sw.flowsFromIP(sourceip,days,hours)

## Modules

Main module (to be imported) is cats.py


Other modules testxxx.py are simple scripts to test the APIs (enabling future regression testing as well as development).


testpxgrid.py : Shows some use cases with the cats ISE-PXGRID class, how they can be used
try textpxgrid.py -h for help.


