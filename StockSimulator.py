import shelve
import robin_stocks
from datetime import datetime


def UTC_seconds(time_string):
	"""Converts UTC time of entry to total seconds to identify active trading hours"""

	hours = time_string[0:2]
	minutes = time_string[3:5]

	hours = hours.lstrip('0')
	minutes = minutes.lstrip('0')

	if not hours:
		hours = '0'

	if not minutes:
		minutes = '0'

	return 60*eval(hours) + eval(minutes)

def opening_time(entry):
	date_time = entry['begins_at']
	return UTC_seconds(date_time[11:16])

def opening_price(entry):
	return entry['open_price']

def closing_price(entry):
	return entry['close_price']

def price_assumption(entry):
	return (high_price(entry) + low_price(entry))/2

def high_price(entry):
	return entry['high_price']

def low_price(entry):
	return entry['low_price']


class SimOrder:

	profit = 0
	trigger = 'immediate'


class SimSell(SimOrder)

	side = 'sell'

	def sell_action(self):
		"""Takes in order object as argument"""

		stock = SimStock.simulation_stocks[self.symbol]
		SimOrder.profit += self.shares*(self.sell_price - self.starting_price)

		stock.shares -= self.shares

		if stock.shares == 0:
			del SimStock.simulation_stocks[self.symbol]


	class sim_limit_sell(SimSell):

		def __init__(self, symbol, shares, sell_price):

			self.symbol = symbol
			self.shares = shares
			self.sell_price = sell_price
			self.sell_action()

	class sim_market_sell(SimSell):

		def __init__(self, symbol, shares, sell_price):

			self.symbol = symbol
			self.shares = shares
			self.sell_price = sell_price
			self.sell_action()

	class sim_stop_loss_less(SimSell):

		trigger = 'stop'

		def __init__(self, symbol, shares, stop_price):

			self.symbol = symbol
			self.shares = shares
			self.stop_price = stop_price
			self.sell_price = sell_price

		
	


class SimStock:

	simulation_stocks = shelve.open('simulation_stocks', writeback=True)

	def __init__(self, symbol, shares, span):
		self.symbol = symbol
		self.shares = shares
		self.pending_sales = 0
		self.pending_buys = 0
		self.price = None #will be set during simulation
		self.starting_price = None #will be set at beginning of simulation
		self.reference_price = None #will be set at beginning of simulation


		self.day = self.get_historicals(self.symbol, 'day', 'Extended')
		self.week = self.get_historicals(self.symbol, 'week')
		self.month = self.get_historicals(self.symbol, 'month')
		self.three_month = self.get_historicals(self.symbol, '3month')
		self.year = self.get_historicals(self.symbol, 'year')
		self.five_year = self.get_historicals(self.symbol, '5year')

		SimStock.simulation_stocks[self.symbol] = self
		SimStock.simulation_stocks.sync()


	def set_price(self, entry):
		self.price = price_assumption(entry)
	
	def set_average_buy_cost(self, span):
		"""Sets 'average buy price' for the sake of a simulation"""
		historical = self.choose_historical(span)
		for entry in historical:
			if opening_time(entry) >= 780:
				self.average_buy_cost = opening_price(entry)
				return

	def set_reference_price(self, price):
		"""sets a reference price for time-increment dependence other than overall performance of stock"""
		self.reference_price = price

	@property
	def equity(self):
		return self.price*self.shares
	
	@property
	def original_equity(self):
		return self.shares*self.average_buy_cost

	@property
	def profit(self):
		return round(self.equity - self.original_equity, 2)
	
	@property
	def available_shares(self):
		return self.shares - self.pending_sales

	@property
	def percent_change(self):
		if self.average_buy_cost != 0:
			return 100*(self.price - self.average_buy_cost)/(self.average_buy_cost)
		else:
			return 'Order pending'


	def choose_historical(self, span):

		if span == 'day':
			return self.day
		if span == 'week':
			return self.week
		if span == 'month':
			return self.month
		if span == '3month':
			return self.three_month
		if span == 'year':
			return self.year
		if span =='5year':
			return self.five_year

	def get_historicals(self,  span, bounds='Regular'):

		return robin_stocks.stocks.get_historicals(self.symbol, span, bounds)

	def historical_generator(self, span):

		history_info = self.choose_historical(span)
		yield from history_info








		







