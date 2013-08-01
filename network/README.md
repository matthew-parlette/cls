network_fix
==========

This is a utility that will pick up the current IP address of a computer and continuously try to get a new IP address until an acceptable one is received.

The purpose of this script is to fix an issue at CLS where a computer will randomly receive a 10.x IP address, when they need a 192. IP address to connect.

There are two files:
*network_fix.py - Source code
*network_fix.exe - Packaged executable for easier deployment
