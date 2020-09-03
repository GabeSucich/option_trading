import robin_stocks
from options import *


def get_stock_historicals(symbol, interval, span):
	"""Returns the historical data for a SYMBOL with data at every time INTERVAL over a given SPAN."""
	assert span in ['day', 'week', 'month', '3month', 'year', '5year']
	assert interval in ['5minute', '10minute', 'hour', 'day', 'week']

	return robin_stocks.stocks.get_historicals(symbol, interval, span)

def stock_historicals_between_dates(all_historicals, starting_date, ending_date):

	relevant_dates = []

	for data_point in all_historicals:

		date = get_historical_date(data_point)

		if is_not_past(date, starting_date) and is_not_past(ending_date, date):

			relevant_dates.append(data_point)

	return relevant_dates





	


	

	








