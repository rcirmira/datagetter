#!/usr/bin/python

import sys, getopt

def main(argv):
   outputdir = ''
   datasource = ''

   try:
      opts, args = getopt.getopt(argv,"hd:o:",["help", "datasource=", "outdir="])
   except getopt.GetoptError:
      print 'datagetter.py -d <datasource> -o <outputdir>'
      sys.exit(2)

   for opt, arg in opts:
      if opt in ( "-h", "--help"):
         print 'test.py -d <datasource> -o <outputdir>'
         sys.exit()
      elif opt in ("-d", "--datasource"):
         datasource = arg
      elif opt in ("-o", "--outdir"):
         outputdir = arg

   if datasource == '' or outputdir == '':
      print 'test.py -d <datasource> -o <outputdir>'
      sys.exit()
   print 'Data Source: ', datasource
   print 'Output Dir: ', outputdir

if __name__ == "__main__":
   main(sys.argv[1:])