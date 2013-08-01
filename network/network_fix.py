#!/usr/bin/python

import argparse
import logging
import os

def main():
  parser = argparse.ArgumentParser(description='Resolve IP-related network issues at CLS.')
  parser.add_argument('-v','--version',action='version',version='1.0')
  parser.add_argument('-d','--debug',action='store_true',help="Show debug log messages")
  parser.add_argument('-l','--logfile',action='store_true',help="Log messages to a log file (in addition to console)")
  args = parser.parse_args()
  
  #Setup logger
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

if __name__ == '__main__':
  main()
