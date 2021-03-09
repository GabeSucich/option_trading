import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from Models.Stocks.StockDay import *
from Stocks.stockhistoricals import *

import Utils.jsonHelper as jh

class StockHistory:

	def __init__(self, symbol, granularity = None):

		self.history = createHistory(jh.loadStockHistoricals(symbol), granularity)

	def getHistory(self):

		return self.history

class RealTimeStockHistory(StockHistory):

	def __init__(self, symbol, granularity, date_list, historyLength = 10):

		full_historicals = jh.loadStockHistoricals(symbol)
		truncated_historicals = truncateHistoricals(full_historicals, date_list, historyLength)
		for date in date_list:
			if date not in truncated_historicals:
				add_date_to_historicals(symbol, truncated_historicals, date)
		self.history = createHistory(truncated_historicals, granularity)



def createHistory(historicals, granularity):

	history = {}

	for date in historicals:

		if granularity == "semi":
			history[date] = SemiStockDay(date, historicals[date])

		elif granularity == "quartile":
			history[date] = QuartileStockDay(date, historicals[date])

		elif granularity == "halfHour":
			history[date] = HalfHourlyStockDay(date, historicals[date])

		else:
			history[date] = StockDay(date, historicals[date])

	return dict(sorted(history.items()))




def truncateHistoricals(full_historicals, date_list, historyLength):

	truncated_data = {}
	dates = list(full_historicals.keys())
	dates.sort()

	if all([date in dates for date in date_list]):

		index = dates.index(date_list[-1])
		dates = dates[:index + 1]

	for date in dates[- (historyLength + len(date_list)):]:
		truncated_data[date] = full_historicals[date]

	return truncated_data

def add_date_to_historicals(symbol, current_historicals, date):

	data_to_add = get_price_data_for_date(date, symbol)
	current_historicals[date] = data_to_add[date]

def get_price_data_for_date(date, symbol):

	data = {}
	all_recent_data = get_all_recent_data(symbol)
	data[date] = all_recent_data[date]
	correct_timezones(data)
	del data[date]["corrected"]
	for key in list(data[date].keys()):
		for attribute, value in data[date][key].items():
			data[date][key][attribute] = eval(value)
	return data





