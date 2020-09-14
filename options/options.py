import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import Utils.login
from Utils.datetime_funcs import *
import json
import robin_stocks_modified as robin_stocks



"""ROBIN STOCKS FUNCTIONS"""

"""PORTFOLIO"""

def load_financials():
	"""Returns portfolio"""
	return robin_stocks.profiles.build_user_profile()


def buying_power():
	"""Returns buying power."""
	financials = load_financials()
	return string_to_rounded(financials['cash'])

"""OPTIONS"""

def current_option_positions(info=None):
	"""Gives holding and option id data for open positions. INSTANT. No market or instrument data"""
	return robin_stocks.options.get_open_option_positions(info)

def tradable_options(symbol):
	"""Return all tradeable options for a single stock"""
	return robin_stocks.options.find_tradable_options_for_stock(symbol)

def options_by_expiration(symbol, expirationDate, optionType='both', info=None):
	"""Gets market and instrument data for option from expiration date. Takes time to load pages."""
	assert all(isinstance(i, str) for i in [symbol, expirationDate, optionType])
	return robin_stocks.options.find_options_for_stock_by_expiration(symbol, expirationDate, optionType, info)

def sorted_options_by_expiration(symbol, expirationDate, optionType, info=None):
	"""Gets all option data sorted in ascending order by strike price. Takes time to load pages."""

	unsorted = options_by_expiration(symbol, expirationDate, optionType, info)
	unsorted.sort(key=lambda dict: float(dict['strike_price']))
	return unsorted

def options_by_strike(symbol, strike, optionType='both', info=None):
	"""Gets all market and instrument data for option from the strike price. Takes time to load pages."""
	assert all(isinstance(i, str) for i in [symbol, strike, optionType])
	return robin_stocks.options.find_options_for_stock_by_expiration(symbol, strike, optionType, info)

def options_by_expiration_and_strike(symbol, expirationDate, strike, optionType='both', info=None):
	"""Gets all market and instrument data for option from expiration and strike price. INSTANT."""
	assert all(isinstance(i, str) for i in [symbol, expirationDate, strike, optionType])
	return robin_stocks.options.find_options_for_stock_by_expiration_and_strike(symbol, expirationDate, strike, optionType, info)


def market_data(symbol, expirationDate, strike, optionType, info=None):
	"""Gets option market data from information. Takes time to load pages."""
	assert all(isinstance(i, str) for i in [symbol, expirationDate, strike, optionType])
	return robin_stocks.options.get_option_market_data(symbol, expirationDate, strike, optionType, info=None)

def market_data_by_id(option_id, info=None):
	"""Gets market data from option id. INSTANT.""" 
	assert type(option_id) == str
	return robin_stocks.options.get_option_market_data_by_id(option_id, info)

def instrument_data(symbol, expirationDate, strike, optionType, info=None):
	"""Gets instrument data from information. Takes time to load pages."""
	assert all(isinstance(i, str) for i in [symbol, expirationDate, strike, optionType])
	return robin_stocks.options.get_option_instrument_data(symbol, expirationDate, strike, optionType, info)

def instrument_data_by_id(option_id, info=None):
	"""Gets instrument data from option id. INSTANT."""
	assert type(option_id) == str
	return robin_stocks.options.get_option_instrument_data_by_id(option_id, info)

def chain_data(symbol, info=None):
	"""Gets chain data for stock. INSTANT. Includes possible expiration dates for options."""
	assert type(symbol) == str
	return robin_stocks.options.get_chains(symbol, info)

def get_list_of_strikes(symbol, expiration_date, option_type="call"):

	unordered_string = options_by_expiration(symbol, expiration_date, option_type, 'strike_price')
	floats = [float(price) for price in unordered_string]
	floats.sort(reverse=False)
	return [str(price) for price in floats]

def get_option_historicals(symbol, expiration_date, strike_price, option_type, span="week", interval="30minute"):
	"""SYMBOL, EXPIRATION_DATE, STRIKE_PRICE, OPTION_TYPE are all strings. Returns data every TEN minutes for each day in the past week. Times are in UTC time."""
	historicals = robin_stocks.options.get_option_historicals(symbol, expiration_date, strike_price, option_type)

	if type(historicals) == dict:

		historical_data = historicals['data_points']

	else:
		historical_data = historicals

	return historical_data

def get_option_historicals_by_id(optionID, span="week", interval="30minute"):
	"""Gets the historical data for an option with OPTIONID. SPAN specifies how far back to get historicals, and interval specifies how often in the day to present data."""
	historicals = robin_stocks.options.get_option_historicals_by_id(optionID, span=span, interval=interval)

	if type(historicals) == dict:

		historical_data = historicals['data_points']

	else:
		historical_data = historicals

	return historical_data

def get_historical_time(data_point):
	"""Returns the time of a DATA_POINT"""

	try:
		return data_point['begins_at'][11:16]
	except:
		return None

def get_historical_date(data_point):
	"""Returns the date of a DATA_POINT"""

	try:
		return data_point['begins_at'][0:10]
	except:
		return None



def formatted_option_historicals(raw_historicals, trade_date):
	"""Returns a formatted version of the RAW_HISTORICALS containing data for a specific TRADE_DATE."""

	daily_data = []

	for data_point in raw_historicals:

		time = get_historical_time(data_point)
		date = get_historical_date(data_point)

		if time:

			if (date == trade_date):

				daily_data.append(data_point)
 

	basic_market_data = {}

	for data_point in daily_data:

		time = utc_to_military(get_historical_time(data_point))
		del data_point['begins_at']
		del data_point['interpolated']
		del data_point['session']
		basic_market_data[time] = data_point

	return {"basic_market_data": basic_market_data}


def possible_expiration_dates(symbol):
	"""Gives a list of strings, each corresponding to a different possible expiration date. INSTANT."""
	return chain_data(symbol, 'expiration_dates')

def expiration_from_length(symbol, time_length):
	"""Takes in a stock symbol and a number of days, and returns the earliest expiration date that is time_length away."""
	possible_expiration_dates_list = possible_expiration_dates(symbol)

	for date in possible_expiration_dates_list:

		if days_away(date) >= time_length:

			return date

"""STOCKS"""

def latest_stock_price(symbol):
	"""Returns share price of stock as float."""

	price_list = robin_stocks.stocks.get_latest_price(symbol)
	return float(price_list[0])









