from options import *
import json

from apscheduler.schedulers.blocking import BlockingScheduler

tracked_stocks = []

def read_json(filename):
	"""FILENAME is the name of a json file containing option information. This function loads the json object into the script 
	to be edited. The return object is the option dictionary to be edited."""

	data_file = open(filename, "r")
	data = json.load(data_file)
	data_file.close()

	return data

def dump_json(updated_dict, filename):
	"""UPDATED_DICT is the option object with updated data. FILENAME is the name of the json file containing the option information.
	Run this function to update json files with new option data."""
	data_file = open(filename, "w")
	json.dump(updated_dict, data_file)
	data_file.close()

	return "{0} successfully updated".format(filename)

def list_tracked_stocks():
	"""Returns a list of all stock symbols for the stocks being tracker"""
	data = read_json("tracked_stocks.json")
	return list(data.keys())

def json_for_stock(symbol):
	"""SYMBOL is a stock symbol (capitalized). Returns the json object from the associated json file."""
	filename = symbol + ".json"
	return read_json(filename)


def ids_for_stock(symbol):
	"""DATA is a JSON object read in from a data file. This function will get a list of id's for each option from this data."""
	data = json_for_stock(symbol)
	ids = []
	for expiration in list(data.keys()):
		for strike in list(data[expiration]['puts'].keys()):
			ids.append(data[expiration]['puts'][strike]['id'])
	for expiration in list(data.keys()):
		for strike in list(data[expiration]['calls'].keys()):
			ids.append(data[expiration]['calls'][strike]['id'])

	return ids



def setup_daily_info():
	"""This function sets up the dictionary of market data to be gathered for the day.""" 

	for stock in list_tracked_stocks():
		tracked_stocks.append({'symbol':stock, 'date': date_to_string(date.today()), 'market_data': []})
		
		stock_data = read_json(JSON_file_name)

def GabeExample2():

	return "Second Example"

def GabeExample():

	return "This is an example function to test merging"



"""Gabe's Work"""

# """Sam's Work"""

def init_options_dict(symbol):
	"""Initializes the options tracking dictionary for the stock with name SYMBOL. Also adds SYMBOL to dictionary of tracked stocks
	in tracked_stocks.json if it does not already exist. Will raise an assertion error if trying to initialize tracking on a stock
	SYMBOL that's already tracked. The options tracking dictionary for the stock SYMBOL is set up with keys representing the expiration 
	dates of all available options. Each expiration date key maps to a dictionary with two keys "puts" and "calls". Each of the "puts"
	and "calls" keys map to a dictionary with keys of strike prices. Each strike price key maps to a dictionary with a key that is the
	Robinhood id for that option, and keys respresenting dates in the form yyyy-mm-dd. Each yyyy-mm-dd key maps to multiple dictionaries
	each with an associated time key in the form hhmm (e.g. the key for 8:00AM is 0800, and 3:30PM is 1530). Each time key maps to the
	market data of the given option at the time supplied by the Robinhood API.

	E.g. At 5:00PM on July 14th, 2020, the market data for the put on the given stock with strike price $200 that expires on August 25th,
	2020 is accessed by the following: this_symbol_dict["20200825"]["puts"]["200"]["20200714"]["1700"]

	A visual of the dictionary layout is shown below:



	this_symbol_dict = {

	'expirationdate1': {
					'puts': {
						'strike price':{
								'id': "this option's id",
								'date1': {
										'hour1': "market_data",
										'hour2': "market_data",
										},
								'date2': {
										'hour1': "",
										'hour2': "",
										}
								}
					},
					'calls': {
						'strike price':{
								'id': "this option's id",
								'date1':{
										'hour1':" market_data",
										'hour2': "market_data",
										},
								'date2': {
										'hour1': "",
										'hour2': "",
										}
								}
					}
				}
}
"""
	alreadyTracked = symbol in list_tracked_stocks()
	assert alreadyTracked == False, "Error, this stock is already tracked"
	return;