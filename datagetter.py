#!/usr/bin/python

import sys
import argparse

def parse_input(argv):
	parser = argparse.ArgumentParser(description='Process getting financial data')
	parser.add_argument('-d', '--datasource', nargs=1, metavar='datasource', help='Source of stock data, can be one of Norgate or Yahoo')
	parser.add_argument('-o', '--outputdir', nargs=1, metavar='outputdir', help='Where data will be stored')
	args = parser.parse_args()
	
	return args

def main(argv):
	inputs = parse_input(argv)

	print 'Data Source: ', inputs.datasource[0]
	print 'Output Dir: ', inputs.outputdir[0]
	
if __name__ == "__main__":
   main(sys.argv[1:])