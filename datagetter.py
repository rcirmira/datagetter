#!/usr/bin/python

import argparse
import os
import sys
import urllib2

from bs4 import BeautifulSoup

# Gets and downloads files
#
def fetch_file(url):
	file_fetcher = urllib2.build_opener()
	file_fetcher.addheaders =  [('User-agent', 'Mozilla/5.0')]
	file_data = file_fetcher.open(url).read()
	return file_data
		
# Obtains html from Wikipedia
# Note: API exist but for my use case. Data returned was not parsable. Preferred to use html
# python-wikitools - http://code.google.com/p/python-wikitools/
# Ex. http://en.wikipedia.org/w/api.php?format=xml&action=query&titles=List_of_S%26P_500_companies&prop=revisions&rvprop=content
def wiki_html(url,file_name):
	module_path = os.path.dirname(os.path.realpath(__file__))
	exchanges_dir = os.path.join(module_path,'exchanges')
	file_path = os.path.abspath(exchanges_dir) + os.sep + file_name
	
	if(os.path.exists(file_path)):
		opener = urllib2.build_opener()
		print ">>>>>>", file_path
		return opener.open("file://" + file_path).read()
	else:
		wiki_html = fetch_file('http://en.wikipedia.org/wiki/'+str(url))
		saved_file = open(file_path , "w")
		saved_file.write(wiki_html)
		saved_file.close()
		return wiki_html

# Get unbiased SP500 symbols
#	
def get_sp500_symbols():
	page_html = wiki_html('List_of_S%26P_500_companies','SP500.html')
	wiki_soup = BeautifulSoup(page_html)
	symbol_table = wiki_soup.find(attrs={'class': 'wikitable sortable'})

	symbol_data_list = list()

	for symbol in symbol_table.find_all("tr"):
		symbol_data_content = dict()	
		symbol_raw_data = symbol.find_all("td")
		td_count = 0
		for symbol_data in symbol_raw_data:
			if(td_count == 0): 
				symbol_data_content['symbol'] = symbol_data.text.encode('utf-8')
			elif(td_count == 1): 
				symbol_data_content['company'] = symbol_data.text.encode('utf-8')
			elif(td_count == 3): 
				symbol_data_content['sector'] = symbol_data.text.encode('utf-8')
			elif(td_count == 4): 
				symbol_data_content['industry'] = symbol_data.text.encode('utf-8')
			elif(td_count == 5):
				symbol_data_content['headquaters'] = symbol_data.text.encode('utf-8')

			td_count += 1

		symbol_data_list.append(symbol_data_content)

	return symbol_data_list[1::]
		
# For now we only care about SP500, but also excluded in the past companies
# Get the list from the wiki
#
# Use Norgate data source but give option to extend later on the code base to get data from Yahoo or any other data provider
def get_symbols(datasource, outputdir):

	print 'Data Source: ', datasource
	print 'Output Dir: ', outputdir
	
	symbols = get_sp500_symbols();
	
	for obj in symbols:
		print 'Getting data for: ', obj[ 'symbol' ]
		
	print 'Finihsed getting data'

def parse_input(argv):
	parser = argparse.ArgumentParser(description='Process getting financial data')
	parser.add_argument('-d', '--datasource', nargs=1, metavar='datasource', help='Source of stock data, For now only Norgate is supported')
	parser.add_argument('-o', '--outputdir', nargs=1, metavar='outputdir', help='Where data will be stored')
	args = parser.parse_args()
	
	return args

def main(argv):
	inputs = parse_input(argv)
	symbols = get_symbols( inputs.datasource[0], inputs.outputdir[0] )
	
if __name__ == "__main__":
   main(sys.argv[1:])