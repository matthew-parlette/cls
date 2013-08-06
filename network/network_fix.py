#!/usr/bin/python

import argparse
import logging
import os
import subprocess
import netifaces as ni
from netaddr import IPNetwork,IPAddress

log = None
blacklist_range = [IPNetwork('10.0.0.0/8')]
whitelist_range = [IPNetwork('192.168.1.0/24')]
max_attempts = 3

def main():
  parser = argparse.ArgumentParser(description='Resolve IP-related network issues at CLS.')
  parser.add_argument('-v','--version',action='version',version='1.0')
  parser.add_argument('-d','--debug',action='store_true',help="Show debug log messages")
  parser.add_argument('-l','--logfile',action='store_true',help="Log messages to a log file (in addition to console)")
  args = parser.parse_args()
  
  #Setup logger
  global log
  log = logging.getLogger('network_fix')
  log.setLevel(logging.DEBUG) if args.debug else log.setLevel(logging.INFO)
  
  #Log Format
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  
  #Log to File
  if args.logfile:
    fh = logging.FileHandler('%s.log' % os.path.basename(__file__))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
  
  #Log to Console
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG) if args.debug else log.setLevel(logging.INFO)
  ch.setFormatter(formatter)
  log.addHandler(ch)
  
  log.debug("Logger initialized")
  
  keep_trying = True
  attempts = 0
  
  while keep_trying and attempts < max_attempts:
    if diagnose_network():
      log.info("All IP Addresses determined to be valid.")
      keep_trying = False
    else:
      log.error("One or more invalid IP addresses were found")
      
      #try for a new ip address
      log.info("Releasing current IP Address...")
      os.popen("ipconfig /release")
      log.info("Requesting a new IP Address...")
      os.popen("ipconfig /renew")
      log.debug("ipconfig returned")
    attempts += 1
  
  log.debug("Script exiting")

def diagnose_network():
  """Get all IP addresses assigned to this system.
  
  If an IP is in the blacklist, return False."""
  
  interfaces = ni.interfaces()
  for nif in interfaces:
    log.debug("Processing interface %s" % nif)
    log.debug("ifaddresses output: %s" % ni.ifaddresses(nif))
    log.debug("ifaddresses keys: %s" % ni.ifaddresses(nif).keys())
    if ni.AF_INET in ni.ifaddresses(nif):
      for addr in ni.ifaddresses(nif)[ni.AF_INET]:
        log.debug("Read IP of %s" % addr['addr'])
        for black_addr in blacklist_range:
          ip = IPAddress(addr['addr'])
          if ip in black_addr:
            log.error("IP Address %s found to be in blacklist range %s" % (ip,black_addr))
            return False
  
  return True

if __name__ == '__main__':
  main()
