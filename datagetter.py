#!/usr/bin/python

import argparse
import os
import QSTK.qstkutil.DataAccess as da
import sys
import urllib2

from bs4 import BeautifulSoup
from datetime import datetime

def timeit( text ):
	if not hasattr( timeit, "start" ):
		timeit.start = datetime.now()
	
	now = datetime.now()
	print "%30s, from start: %16s, %s" % ( str( now ), str( now-timeit.start ), text )
	
# Obtains html from Wikipedia
# Note: API exist but for my use case. Data returned was not parsable. Preferred to use html
# python-wikitools - http://code.google.com/p/python-wikitools/
# Ex. http://en.wikipedia.org/w/api.php?format=xml&action=query&titles=List_of_S%26P_500_companies&prop=revisions&rvprop=content
def wiki_html( url ):
	file_fetcher = urllib2.build_opener()
	file_fetcher.addheaders =  [('User-agent', 'Mozilla/5.0')]
	wiki_html = file_fetcher.open( 'http://en.wikipedia.org/wiki/'+str( url ) ).read()
	return wiki_html

# Get unbiased SP500 symbols
#	
def get_sp500_symbols():
	page_html = wiki_html( 'List_of_S%26P_500_companies' )
	wiki_soup = BeautifulSoup( page_html )
	symbol_table = wiki_soup.find( attrs={ 'class': 'wikitable sortable' } )

	symbol_data_list = list()

	for symbol in symbol_table.find_all( 'tr' ):
		symbol_data_content = dict()	
		symbol_raw_data = symbol.find_all( 'td' )
		td_count = 0
		for symbol_data in symbol_raw_data:
			if( td_count == 0 ): 
				symbol_data_content['symbol'] = symbol_data.text.encode( 'utf-8' )
			elif( td_count == 1 ): 
				symbol_data_content['company'] = symbol_data.text.encode( 'utf-8' )
			elif( td_count == 3 ): 
				symbol_data_content['sector'] = symbol_data.text.encode( 'utf-8' )
			elif( td_count == 4 ): 
				symbol_data_content['industry'] = symbol_data.text.encode( 'utf-8' )
			elif( td_count == 5 ):
				symbol_data_content['headquaters'] = symbol_data.text.encode( 'utf-8' )

			td_count += 1

		symbol_data_list.append( symbol_data_content )

	return symbol_data_list[1::]

# Get market data for a given symbol and store it in provided directory
#
# There are 3 possible options
#   - if the file exists, get latest date and append missing data
#   - if the file doesn't exist, get full data
#   - If the data is up to date, do nothing

def get_data( dir, symbol ):
	timeit( '>>>>>>>>>>>>>>>>>>>>>' )
	timeit( 'Getting data for: %s' % symbol )	
	symbol_file = os.path.abspath( dir ) + os.sep + symbol + '.csv'
	
	if os.path.exists( symbol_file ):
		# File exists, get latest data and process
		timeit( 'File: %s exists' % symbol_file )
	else:
		# File doesn't exist, get full data
		timeit( 'File: %s does not exist' % symbol_file )
		try:
			f = open( symbol_file, "w" )
		except IOError as e:
			timeit( 'Cannot create file: %s due to the error: %s data will be missing' % ( symbol_file, format(e) ) )
			return
			
		f.close()
	
def create_dir( module_path, folder ):
	dir = os.path.join( module_path,folder )
	print dir
	if not os.path.exists( dir ):
		timeit( 'Creating directory: %s' % dir )
		os.makedirs( dir )
	else:
		timeit( 'Directory exists: %s' % dir )
	
	return dir
		
# For now we only care about SP500, but also excluded in the past companies
# Get the list from the wiki
#
# Use Norgate data source but give option to extend later on the code base to get data from Yahoo or any other data provider
def get_symbols( datasource, outputdir ):
	timeit( 'Data Source: %s' % datasource )
	timeit( 'Output Dir: %s' % outputdir )
	
	dataobj = da.DataAccess( datasource )
	
	symbols = get_sp500_symbols()
	timeit( 'Finished getting symbols' )
		
	sp500_data_dir = create_dir( outputdir, 'sp500_data' )
	
	for obj in symbols:
		get_data( sp500_data_dir, obj[ 'symbol' ] )
		
	timeit( 'Finished getting data' )

def parse_input(argv):
	parser = argparse.ArgumentParser( description='Process getting financial data' )
	parser.add_argument( '-d', '--datasource', nargs=1, metavar='datasource', help='Source of stock data, For now only Norgate is supported', default='Norgate'	)
	parser.add_argument( '-o', '--outputdir', nargs=1, metavar='outputdir', help='Where data will be stored', default=os.path.dirname( os.path.realpath( __file__ ) ) )
	args = parser.parse_args()
	
	return args
	
def main( argv ):
	inputs = parse_input( argv )
	symbols = get_symbols( inputs.datasource, inputs.outputdir )
	
if __name__ == "__main__":
	timeit( 'Start' )
	main( sys.argv[1:] )