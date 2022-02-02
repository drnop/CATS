# CATS
Cisco API Tools for Security
... beta version

cats.py :  Collection of classes interacting with Cisco Security APIs.

The objective is to encapsulate complexities and differences across different APIs, to make it easy to write code without knowing
details about each APIs, how it authenticates, time formats etc.

Main module (to be imported) is cats.py

Other modules testxxx.py are simple scripts to test the APIs (enabling future regression testing as well as development).

Example:

testpxgrid.py : Shows some use cases with the cats ISE-PXGRID class, how they can be used
try textpxgrid.py -h for help.


