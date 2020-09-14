import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from options import *
from Utils import login
from Utils.datetime_funcs import *
import json
import holidays

closed_holidays = ["New Year's Day", "Martin Luther King Jr. Day", "Independence Day", "Thanksgiving", "Memorial Day", "Labor Day", "Christmas Day", "Washington's Birthday"]

"""Functions for retrieving and updating information in JSON files."""

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
	data = read_json("optionJSON/tracked_stocks.json")
	return list(data.keys())

def get_json_object(symbol):
	"""Returns the json object from the associated json file of name SYMBOL.json"""
	return read_json(json_filename(symbol))

def json_filename(symbol):
	"""Appends .json to the string SYMBOL"""
	return "optionJSON/" + symbol + ".json"

"""Functions for generating different types of keys from a json stock object"""

def expiration_generator(json_data):
	"""Yields each expiration date in the JSON_DATA dictionary."""
	yield from list(json_data.keys())

def future_expiration_generator(json_data):

	all_expirations = list(expiration_generator(json_data))
	return [date for date in all_expirations if is_future(date)]

def put_strike_generator(json_data, expiration):
	"""Yields the strike price for every put with a give EXPIRATION from a JSON_DATA dictionary."""

	yield from list(json_data[expiration]['puts'].keys())

def call_strike_generator(json_data, expiration):
	"""Yields the strike price for every call with a give EXPIRATION from a JSON_DATA dictionary."""
	yield from list(json_data[expiration]['calls'].keys())

def option_generator_for_expiration(json_data, expiration):
	"""Yields the dictionary for every option with the given EXPIRATION in the JSON_DATA dictionary."""
	for put_strike in put_strike_generator(json_data, expiration):
		yield json_data[expiration]['puts'][put_strike]

	for call_strike in call_strike_generator(json_data, expiration):
		yield json_data[expiration]['calls'][call_strike]

def option_generator(json_data):
	"""Yields the dictionary for every single option in the JSON_DATA dictionary."""
	for expiration in expiration_generator(json_data):

		yield from option_generator_for_expiration(json_data, expiration)

def future_option_generator(json_data):
	"""Yields the dictionary for every single option with an expiration date in the future from a JSON_DATA dictionary."""

	for expiration in future_expiration_generator(json_data):

		yield from option_generator_for_expiration(json_data, expiration)

def id_generator_for_expiration(json_data, expiration):

	for option in option_generator_for_expiration(json_data, expiration):

		yield option['id']

def id_generator(json_data):
	"""JSON_DATA is a JSON object read in from a data file. This function will get a list of id's for each option from this data."""

	for option in option_generator(json_data):
		yield option['id']

def future_id_generator(json_data):
	"""JSON_DATA is a JSON object read in from a data file. This function will get a list of id's for each option from this data that has not expired."""
	for option in future_option_generator(json_data):
		yield option['id']


"""Functions which gather information from the Robinhood API."""

# def new_market_data(stock_data):
# 	"""STOCK_DATA is a single dictionary from the "tracked_stocks" list which holds the daily data for a single stock. TIME is a time of data collection that is ALREADY ROUNDED
# 	to the nearest storage time. This function calls on the market data for each id key in stock data, gathers the option market data, and adds it to the stock_data as the value of
# 	the appropriate time key."""
# 	symbol = stock_data['symbol']
# 	market_dict = stock_data['market_data']
# 	time = round_to_thirty(get_military_time())

# 	for option_id in list(market_dict.keys()):
# 		try:
# 			market_data = market_data_by_id(option_id)
# 			market_dict[option_id][time] = market_data
# 		except:
# 			print("There was an error storing the market data for the option id {0} for {1} at {2}".format(option_id, symbol, time))

# def update_all_data():
# 	"""Adds new market data for every tracked stock at the current time."""

# 	if market_is_open():

# 		for stock_data in tracked_stocks:
# 			new_market_data(stock_data)

# -------------------------------------------------------- #

def historical_dates_available(historicals_list):
	"""Takes in a HISTORICALS_LIST of option historicals and returns a list of dates which are available with information in the list."""
	dates = []
	for data_point in historicals_list:

		historical_date = get_historical_date(data_point)

		if historical_date not in dates:
			dates.append(historical_date)

	return dates

def select_first_valid_id_from_expiration(json_data, expiration):
	"""Picks out the first id in a JSON_DATA dictionary fo the given EXPIRATION date."""

	ids = id_generator_for_expiration(json_data, expiration)
	market_data = None

	while not market_data:
		option_id = next(ids, None)
		market_data = get_option_historicals_by_id(option_id)
		if not option_id:
			return None

	return option_id

def all_available_historical_dates(json_data, expiration):
	"""Will find all the available historicals for the """
	test_id = select_first_valid_id_from_expiration(json_data, expiration)
	if not test_id:

		return None

	option_historicals = get_option_historicals_by_id(test_id)
	return historical_dates_available(option_historicals)

def new_basic_data_for_option(json_data, option, date_list):
	"""Updates the daily data for an OPTION in the JSON_DATA for each date in the DATE_LIST"""

	option_id = option['id']
	raw_historicals = get_option_historicals_by_id(option_id)

	for trade_date in date_list:

		if trade_date not in option:

			if raw_historicals:
				
				formatted = formatted_option_historicals(raw_historicals, trade_date)
				if not formatted:
					print("{} out of range of historical data.".format(trade_date))
				else:
					basic_market_data = formatted["basic_market_data"]
					option[trade_date] = basic_market_data


def new_basic_data_for_expiration(json_data, expiration, date_list):
	"""Updates the data for each date in the DATE_LIST for all options with a given EXPIRATION date in a given JSON_DATA set."""

	for option in option_generator_for_expiration(json_data, expiration):

		new_basic_data_for_option(json_data, option, date_list)

def new_basic_data(symbol, json_data, date_list):
	"""JSON_DATA is a dictionary read in from a JSON file. This function will collect basic data for the given stock on the given day and add it into the dictionary."""
	
	for expiration in future_expiration_generator(json_data):

		new_basic_data_for_expiration(json_data, expiration, date_list)

	print("Saving json with daily data for " + symbol)
	dump_json(json_data, json_filename(symbol))
	

def update_all_basic_data(date_list, symbols=[]):
	"""Updates daily option data for each date specified in *args. If EXCLUDED is non-empty, each tracked stock not contained in the excluded list will be updated.
	If included is non-empty, only stocks in the included list will be updated. Excluded and included cannot both be non-empty."""


	if not symbols:

		symbols = list_tracked_stocks()


	for symbol in symbols:

		if symbol not in list_tracked_stocks():

			print("Must initialize {} JSON file first".format(symbol))

		else:

			print("Starting data collection for {}".format(symbol))
			json_data = get_json_object(symbol)
			new_basic_data(symbol, json_data, date_list)



def update_expirations(symbol):
	"""Adds new expiration dates to the JSON file for the stock with the argument SYMBOL."""

	data = get_json_object(symbol)
	all_options = tradable_options(symbol)

	def generate_new_expiration_dates():
		"""Generator function which yields all of the expiration dates for the stock that are active on robinhood but not present in the json file"""

		current_expirations = possible_expiration_dates(symbol) # Gets list of expiration dates in CHRONOLOGICAL order
		tracked_expirations = list(expiration_generator(data))

		for date in current_expirations:

			if date not in tracked_expirations:
				yield date

	new_expiration_dates = list(generate_new_expiration_dates())

	for expiration in new_expiration_dates: # Real code

		options = expiration_date_filter(all_options, expiration)

		add_single_expiration_dict(data, expiration)
		add_put_and_call_keys_for_expiration(data, expiration)
		add_strike_prices_and_ids_for_expiration(options, data, expiration)

		available_historical_dates = all_available_historical_dates(data, expiration)

		if not available_historical_dates:

			return print("No new expiration dates for {}".format(symbol))

		new_basic_data_for_expiration(data, expiration, available_historical_dates)

		print("{0} added to expiration dates of {1}".format(expiration, symbol))

	if new_expiration_dates:

		print("Updating JSON with new expiration dates for {}".format(symbol))
		dump_json(data, json_filename(symbol)) # Real code
		# dump_json(stock_data, "ACB.json") # Test code
	else:

		print("No new expiration dates for {}".format(symbol))

def update_expirations_for_all(symbols = []):
	"""Adds new expiration_dates to all tracked symbols"""
	if symbols == []:
		symbols = list_tracked_stocks()

	for symbol in symbols:

		print("Updating expirations for {}".format(symbol))
		update_expirations(symbol)


def update_strike_prices_for_expiration(symbol, json_data, tradable_options, expiration):
	"""For a single EXPIRATION date and a list of TRADABLE_OPTIONS for the SYMBOL, updates the JSON_DATA with all new strike prices."""

	all_calls = [option for option in tradable_options if option['expiration_date'] == expiration and option['type'] == 'call']
	contained_call_strikes = list(call_strike_generator(json_data, expiration))

	all_puts = [option for option in tradable_options if option['expiration_date'] == expiration and option['type'] == 'put']
	contained_put_strikes = list(put_strike_generator(json_data, expiration))

	for call in all_calls:

		call_strike = call['strike_price']

		if call_strike not in contained_call_strikes:

			option_id = call['id']
			json_data[expiration]['calls'][call_strike] = {'id': option_id}
			option = json_data[expiration]['calls'][call_strike]
			historicals = get_option_historicals_by_id(option_id)

			if historicals:
				print(option_id)
				date_list = historical_dates_available(historicals)
				new_basic_data_for_option(json_data, option, date_list)

	for put in all_puts:

		put_strike = put['strike_price']

		if put_strike not in contained_put_strikes:

			option_id = put['id']
			json_data[expiration]['puts'][put_strike] = {'id': option_id}
			option = json_data[expiration]['puts'][put_strike]
			historicals = get_option_historicals_by_id(option_id)

			if historicals:
				print(option_id)
				date_list = historical_dates_available(historicals)
				new_basic_data_for_option(json_data, option, date_list)

def update_strikes_for_all(symbols=[]):
	"""Adds new strike prices to the json_data for all SYMBOLS. If symbols, updates for all symbols."""
	if not symbols:

		symbols = list_tracked_stocks()

	for symbol in symbols:

		print('Updating strike prices for {}'.format(symbol))
		json_data = get_json_object(symbol)
		all_options = tradable_options(symbol)

		for expiration in future_expiration_generator(json_data):

			update_strike_prices_for_expiration(symbol, json_data, all_options, expiration)

		dump_json(json_data, json_filename(symbol))


def daily_update(date_list, symbols = []):
	if type(date_list) == str:
		date_list = [date_list]

	assert type(date_list) == list, "date_list must be a list"
	if not symbols:

		symbols = list_tracked_stocks()

	print(date_list)
	update_all_basic_data(date_list, symbols)
	update_expirations_for_all(symbols)
	update_strikes_for_all(symbols)
	check_all_data(symbols)

def check_data(symbol):

	error_count = 0

	data = get_json_object(symbol)

	for expiration_date in expiration_generator(data):

		if data[expiration_date] == {} or data[expiration_date]['calls'] == {} or data[expiration_date]['puts'] == {}:

			print("There is an issue with the expiraiton of {0} for {1}".format(expiration_date, symbol))
			error_count += 1


		for call in call_strike_generator(data, expiration_date):

			if data[expiration_date]['calls'][call] == {}:
				print("There is an issue with the ${0} call with expiration date {1} for {2}".format(call, expiration_date, symbol))
				error_count += 1

		for put in put_strike_generator(data, expiration_date):
			if data[expiration_date]['puts'][put] == {}:
				print("There is an issue with the ${0} put with expiration date {1} for {2}".format(put, expiration_date, symbol))
				error_count += 1

	return error_count

def check_all_data(symbols=[]):

	if symbols == []:

		symbols = list_tracked_stocks()

	for symbol in symbols:

		print("Checking data for " + symbol)
		error_count = check_data(symbol)
		if error_count == 0: 
			print("No errors found for " + symbol)

def remove_invalid_dates_for_option(option):

	option_id = option["id"]
	option_keys = list(option.keys())

	if "scrubbed" not in option_keys:

		instrument_data = instrument_data_by_id(option_id)

		if instrument_data:
			
			date_created = instrument_data["created_at"][:10]
			time_created = float(utc_to_military(instrument_data["created_at"][11:16]))


			for date in [date for date in option_keys if date != "id"]:

				if not is_not_past(date, date_created):

					del option[date]

				elif (date_created == date):

					if time_created >= 630:

						del option[date]

			option["scrubbed"] = "complete"

		

def remove_invalid_dates_for_expiration(json_data, expiration):

	for option in option_generator_for_expiration(json_data, expiration):

		remove_invalid_dates_for_option(option)

def remove_invalid_dates_from_json(json_data):

	for expiration in expiration_generator(json_data):

		remove_invalid_dates_for_expiration(json_data, expiration)

def remove_all_invalid_dates(symbols = []):

	if not symbols:

		symbols = list_tracked_stocks()

	for symbol in symbols:

		print("Removing invalid data for " + symbol)
		data = get_json_object(symbol)
		remove_invalid_dates_from_json(data)
		print("Saving scrubbed data for " + symbol)
		dump_json(data, json_filename(symbol))



		
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
	dct = {}
	add_all_expiration_dicts(dct, symbol)
	add_put_and_call_keys(dct)
	add_strike_prices_and_ids(dct, symbol)
	dump_json(dct, json_filename(symbol))
	# keep below lines commented out until testing is complete
	add_to_tracked_stocks_json(symbol)
	print("{0} initialized!".format(symbol))
	return;

def add_to_tracked_stocks_json(symbol):
	"""adds the stock SYMBOL to the list of tracked stocks in tracked_stocks.json 
	WARNING: never call this function unless the stock SYMBOL is truly tracked"""
	trackedStocksDict = read_json("optionJSON/tracked_stocks.json");
	trackedStocksDict[symbol] = chain_data(symbol, info="id");
	dump_json(trackedStocksDict, "optionJSON/tracked_stocks.json");

def add_single_expiration_dict(dct, expiration):
	"""Adds EXPIRATION date to the json DCT."""

	dct[expiration] = {}


def add_all_expiration_dicts(dct, symbol):
	"""Returns a dictionary for the stock SYMBOL with keys corresponding to each option expiration date"""
	expirationDates = possible_expiration_dates(symbol)

	for expiration in expirationDates:
		add_single_expiration_dict(dct, expiration)

def add_put_and_call_keys_for_expiration(dct, expiration):
	"""Adds the keys for puts and calls to a specific EXPIRATION dictionary within a larger json DCT."""

	dct[expiration]['calls'] = {}
	dct[expiration]['puts'] = {}

def add_put_and_call_keys(dct):
	"""Takes a dictionary DICT with expiration date keys and adds "puts" and "calls" keys to each expiration date"""
	for expirationDate in dct.keys():
		add_put_and_call_keys_for_expiration(dct, expirationDate)

def expiration_date_filter(all_options, expirationDate):
	"""Takes a list of ALL_OPTIONS, and returns a list of only those with the argument EXPIRATIONDATE"""
	return [option for option in all_options if option['expiration_date'] == expirationDate]

def add_strike_prices_and_ids_for_expiration(option_list, dct, expiration):
	"""Takes in a OPTION_LIST of all options with the given EXPIRATION, and adds the options to the DCT"""
	for option in option_list:

		strike_price = option['strike_price']
		option_id = option['id']
		option_type = option['type']

		if option_type == 'call':
			dct[expiration]['calls'][strike_price] = {'id': option_id}
		elif option_type == 'put':
			dct[expiration]['puts'][strike_price] = {'id': option_id}


def add_strike_prices_and_ids(dct, symbol):
	"""Takes a dictionary DICT for stock SYMBOL with keys "calls" for each expiration date and maps call strike prices
	to each "calls" key"""

	all_options = tradable_options(symbol)

	for expiration in dct.keys():

		options = expiration_date_filter(all_options, expiration)

		add_strike_prices_and_ids_for_expiration(options, dct, expiration)

def round_to_thirty(str_time):
	"""STR_TIME is a time in the format HHMM. This function rounds down to the nearest half hour."""
	minutes = int(str_time[2:])
	if minutes//30 == 1:
		rounded = "30"
	else:
		rounded = "00"

	return str_time[0:2] + rounded

def format_strike_price(strike_price):

	if "." not in strike_price:

		strike_price += ".0000"
		return strike_price

	else:

		decimal_index = strike_price.index('.')

		missing_places = 5 - (len(strike_price) - decimal_index)

		for i in range(missing_places):

			strike_price += "0"

		return strike_price

def get_holiday_dates(years=[int(current_year())]):
	"""Gets the date for each holiday in the current year on which the stock market is closed."""
	assert all([type(year) == int for year in years]), "All argument YEARS must be integers"
	holiday_dates = []
	for date, name in sorted(holidays.US(state='CA', years=years).items()):

		if name in closed_holidays:

			holiday_dates.append(date_to_string(date))

	return holiday_dates

def market_is_open():
	"""Function which determines if the market is open on a weekday or not. Filters out holidays."""

	return date_to_string(current_date()) not in closed_dates