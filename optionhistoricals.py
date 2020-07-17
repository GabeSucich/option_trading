from options import *
import json

"""Gabe's Work"""

tracked_stocks = []
store_times = ["0630", "0700", "0730", "0800", "0830", "0900", "0930", "1000", "1030", "1100", "1130", "1200", "1230", "1300"]

"""JSON HANDLING"""

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
	data = read_json("stockJSON/tracked_stocks.json")
	return list(data.keys())

def get_json_object(symbol):
	"""Returns the json object from the associated json file of name SYMBOL.json"""
	return read_json(json_filename(symbol))

def json_filename(symbol):
	"""Appends .json to the string SYMBOL"""
	return "stockJSON/" + symbol + ".json"

def expiration_generator(json_data):
	yield from list(json_data.keys())

def put_strike_generator(json_data, expiration):
	yield from list(json_data[expiration]['puts'].keys())

def call_strike_generator(json_data, expiration):
	yield from list(json_data[expiration]['calls'].keys())

def option_generator(json_data):
	for expiration in expiration_generator(json_data):
		for put_strike in put_strike_generator(json_data, expiration):
			yield json_data[expiration]['puts'][put_strike]

		for call_strike in call_strike_generator(json_data, expiration):
			yield json_data[expiration]['calls'][call_strike]

def future_option_generator(json_data):

	all_expirations = list(expiration_generator(json_data))
	unexpired = [date for date in all_expirations if is_not_past(date)]

	for expiration in unexpired:

		for put_strike in put_strike_generator(json_data, expiration):
			yield json_data[expiration]['puts'][put_strike]

		for call_strike in call_strike_generator(json_data, expiration):
			yield json_data[expiration]['calls'][call_strike]


def id_generator(json_data):
	"""JSON_DATA is a JSON object read in from a data file. This function will get a list of id's for each option from this data."""

	for option in option_generator(json_data):
		yield option['id']


def setup_daily_info():
	"""This function sets up the dictionary of market data to be gathered for the day.""" 

	for symbol in list_tracked_stocks():

		today = date_to_string(date.today())
		stock_tracker = {'symbol':symbol, 'date': today, 'market_data': {}}

		
		stock_data = get_json_object(symbol) # Real code
		ids = id_generator(stock_data) # Real code
		# ids = id_generator(read_json("ExampleJSON/DIA.json")) # Test code
		
		for option_id in ids:
			stock_tracker['market_data'][option_id] = {}

		tracked_stocks.append(stock_tracker)

def clear_daily_info():
	"""Clears out tracked_stocks list for next day"""

	tracked_stocks = []


def update_stock_json(tracked_data):
	"""TRACKED_DATA is a single dictionary from the "tracked_stocks" list which holds the daily data for a single stock. This function will go into the
	associated json file and add the data into the appropriate parts of the json object."""
	symbol = tracked_data['symbol']
	date = tracked_data['date']
	daily_data = tracked_data['market_data']
	json_data = get_json_object(symbol) # Real code
	# json_data = read_json("ExampleJSON/DIA.json") # Test code
	for option in future_option_generator(json_data):
		option_id = option['id']
		option_data = daily_data[option_id]
		option[date] = option_data

	dump_json(json_data, json_filename(symbol)) # Real code
	# dump_json(json_data, "ExampleJSON/DIA.json") # Test code


def update_all_json():
	"""Updates each stock json file with the new data in the tracked stocks list."""

	for stock_data in tracked_stocks:
		update_stock_json(stock_data)

"""ROBINHOOD DATA COLLECTION"""

def new_market_data(stock_data):
	"""STOCK_DATA is a single dictionary from the "tracked_stocks" list which holds the daily data for a single stock. TIME is a time of data collection that is ALREADY ROUNDED
	to the nearest storage time. This function calls on the market data for each id key in stock data, gathers the option market data, and adds it to the stock_data as the value of
	the appropriate time key."""

	market_dict = stock_data['market_data']
	time = round_to_thirty(get_military_time())

	for option_id in list(market_dict.keys()):

		market_data = market_data_by_id(option_id)
		market_dict[option_id][time] = market_data

def update_all_data():

	for stock_data in tracked_stocks:
		new_market_data(stock_data)


"""Datetime functions"""

def round_to_thirty(str_time):
	"""STR_TIME is a time in the format HHMM. This function rounds down to the nearest half hour."""
	minutes = int(str_time[2:])
	if minutes//30 == 1:
		rounded = "30"
	else:
		rounded = "00"

	return str_time[0:2] + rounded


# """Sam's Work"""

def init_stock(symbol):
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
	print("Finding expiration dates of options")
	expirationDatesDict = expiration_dates_dict(symbol)
	print("Adding puts and calls keys")
	putsAndCallsDict = add_puts_and_calls_keys(expirationDatesDict)
	print("Adding strike prices for calls")
	finalDict = add_strike_prices_and_ids(putsAndCallsDict, symbol)

	dump_json(finalDict, json_filename(symbol))
	# keep below lines commented out until testing is complete
	add_to_tracked_stocks_json(symbol)
	print("{0} initialized!".format(symbol))
	return;

def add_to_tracked_stocks_json(symbol):
	"""adds the stock SYMBOL to the list of tracked stocks in tracked_stocks.json 
	WARNING: never call this function unless the stock SYMBOL is truly tracked"""
	trackedStocksDict = read_json("tracked_stocks.json");
	trackedStocksDict[symbol] = chain_data(symbol, info="id");
	dump_json(trackedStocksDict, "tracked_stocks.json");

def expiration_dates_dict(symbol):
	"""Returns a dictionary for the stock SYMBOL with keys corresponding to each option expiration date"""
	newDict = {}
	expirationDates = possible_expiration_dates(symbol)
	for date in expirationDates:
		newDict[date] = {}
	print(newDict);
	return newDict

def add_puts_and_calls_keys(dict):
	"""Takes a dictionary DICT with expiration date keys and adds "puts" and "calls" keys to each expiration date"""
	for expirationDate in dict.keys():
		dict[expirationDate]["puts"] = {}
		dict[expirationDate]["calls"] = {}
	return dict

def add_strike_prices_and_ids(dict, symbol):
	"""Takes a dictionary DICT for stock SYMBOL with keys "calls" for each expiration date and maps call strike prices
	to each "calls" key"""

	for expirationDate in dict.keys():

		for option in sorted_options_by_expiration(symbol, expirationDate, "call"):

			strikePrice = option['strike_price']
			option_id = option['id']

			if not market_data_by_id(option_id):
				print('Option passed documentation but is null')

			else:
				market_data_by_id(option_id)
				dict[expirationDate]["calls"][strikePrice] = {'id': option_id}
				print("Found a strike price")

	for expirationDate in dict.keys():
		for option in sorted_options_by_expiration(symbol, expirationDate, "put"):
			
			strikePrice = option['strike_price']
			option_id = option['id']

			if not market_data_by_id(option_id):
				print('Option passed documentation but is null')

			else:
				market_data_by_id(option_id)
				dict[expirationDate]["puts"][strikePrice] = {'id': option_id}
				print("Found a strike price")
				
	
	return dict
