#!/usr/bin/python

import sys, getopt

def main(argv):
   outputdir = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",[@odir="])
   except getopt.GetoptError:
      print 'datagetter.py -ds <datasource> -o <outputdir>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ( "-?", "-h", "--help"):
         print 'test.py -ds <datasource> -o <outputdir>'
         sys.exit()
      elif opt in ("-ds", "--datasource"):
         datasource = arg
      elif opt in ("-o", "--outdir"):
         outputdir = arg
   print 'Data Source: ', datasource
   print 'Output Dir: ', outputdir

if __name__ == "__main__":
   main(sys.argv[1:])