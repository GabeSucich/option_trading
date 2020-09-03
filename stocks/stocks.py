
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import robin_stocks_modified as robin_stocks
from Utils.datetime_funcs import *
from Utils import login

def get_stock_historicals(symbol, interval, span):
	"""Returns the historical data for a SYMBOL with data at every time INTERVAL over a given SPAN."""
	assert span in ['day', 'week', 'month', '3month', 'year', '5year']
	assert interval in ['5minute', '10minute', 'hour', 'day', 'week']

	return robin_stocks.stocks.get_stock_historicals(symbol, interval, span)

def stock_historicals_between_dates(all_historicals, starting_date, ending_date):

	relevant_dates = []

	for data_point in all_historicals:

		date = get_historical_date(data_point)

		if is_not_past(date, starting_date) and is_not_past(ending_date, date):

			relevant_dates.append(data_point)

	return relevant_dates

def get_instrument_data(symbol):

	all_matches = robin_stocks.stocks.find_instrument_data(symbol)

	for match in all_matches:

		if match["symbol"] == symbol:

			return match

	return null

def get_latest_price(symbol, includeExtendedHours=True):

	string_array = robin_stocks.stocks.get_latest_price(symbol, includeExtendedHours)
	return eval(string_array[0])

def get_splits(symbol):

	return robin_stocks.stocks.get_splits(symbol)









	


	

	








