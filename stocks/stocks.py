
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import robin_stocks_modified as robin_stocks
from Utils.datetime_funcs import *
from Utils import login

"""Wrappers for bare robin_stocks functions"""

def get_stock_historicals(symbol, interval="5minute", span="week"):
	"""Returns the historical data for a SYMBOL with data at every time INTERVAL over a given SPAN."""
	assert span in ['day', 'week', 'month', '3month', 'year', '5year']
	assert interval in ['5minute', '10minute', 'hour', 'day', 'week']

	historicals = robin_stocks.stocks.get_stock_historicals(symbol, interval, span)
	process_historicals(historicals)
	return historicals

def get_instrument_data(symbol):
	"""Gets all relevant instrument data for symbol."""

	all_matches = robin_stocks.stocks.find_instrument_data(symbol)

	if not all_matches[0]:
		return None

	for match in all_matches:

		if match["symbol"] == symbol:

			return match

	return None

def get_latest_price(symbol, includeExtendedHours=True):

	string_array = robin_stocks.stocks.get_latest_price(symbol, includeExtendedHours)
	return eval(string_array[0])

def get_splits(symbol):

	return robin_stocks.stocks.get_splits(symbol)

"""These functions help to manipulate data from the API calls."""

def process_historicals(historicals):
	"""Mutates historical data from Robinhood. This function can be added to over time to enable new functionality."""
	for data_point in historicals:

		date = get_historical_date(data_point)
		time = utc_to_military(get_historical_time(data_point))
		data_point["date"] = date
		data_point["time"] = time
		del data_point["begins_at"]
		del data_point["session"]
		del data_point["interpolated"]
		del data_point["symbol"]


def bound_historicals(all_historicals, start_date=None, end_date=None):
	"""Returns the historical data of ALL_HISTORICALS filtered to be bounded by the starting and ending dates."""

	assert start_date or end_date, "stock_historicals_between_dates must have some boundary date provided"

	def isValid(date):
		"""This function will return the validity of the argument DATE based on which of starting_date and ending_date have been passed to the enclosing function."""

		if end_date and start_date:

			return is_not_past(date, start_date) and is_not_past(end_date, date)

		elif not end_date:

			return is_not_past(date, start_date)

		else:
			return is_not_past(end_date, date)


	relevant_dates = []

	for data_point in all_historicals:

		date = data_point["date"]

		if isValid(date):

			relevant_dates.append(data_point)

	return relevant_dates


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








	


	

	








