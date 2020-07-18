import shelve
import robin_stocks
from datetime import date, datetime
import atexit
import math
import getpass
import json

def login():

	data_file = open("credentials.json", "r")
	data = json.load(data_file)
	data_file.close()
	robin_stocks.login(data["username"], data["password"])
	print("Logged In")

login()

"""Notes:
When looking up options, id key in dictionary is 'id'
When examining options as holding, id key is 'option_id'.

MARKET DATA: Price information on option. Does not include strike price or expiration date. DOES NOT include id.
INSTRUMENT DATA: Gives information on expiration and strike price, but not market data. Includes id.
"""

"""SHELVES"""

open_options = shelve.open('open_options', writeback=True)
"""A dictionary for owned option positions. Keys are option ids and values are option objects"""

open_orders = shelve.open('open_orders', writeback=True)

def shelve_closer():
	open_options.close()
	open_orders.close()

def alter_shelve(shelve, keyword, key=None, value=None):
	"""Alters the shelve according to the keyword: 'add' or 'remove'."""
	assert keyword in ['add', 'remove', 'clear']
	assert type(keyword) == str
	if keyword == 'clear':
		shelve.clear()
	elif keyword == 'add':
		shelve[key] = value
	else:
		del shelve[key]
	shelve.sync()
		

atexit.register(shelve_closer)


"""UPDATE FUNCTIONS"""

def refresh_holdings():
	"""Clears holdings and updates dictionary from current holdings."""

	alter_shelve(open_options, 'clear')

	for option in current_option_positions():

		Option(option)

def sell_option(option, quantity, limit_price):

	Sell(option.symbol, option.type, option.expiration_date, option.strike_price, quantity, limit_price)


def set_limit_sell_orders(target_percent, day_trade_protection):

	for option in list(open_options.values()):

		option.limit_sell_all(target_percent)


"""HELPER FUNCTIONS"""

def apply_to_options(func):
	"""Applies func to each option in holdings. func must take in a single option-object as its argument."""

	for option in open_options.keys():

		func(options)

def string_to_rounded(strng):
	"""Takes in a string and returns its numerical value rounded to 2 decimal places"""
	unrounded = eval(strng)
	return round(unrounded, 2)

def round_to_tenth(price):
	"""Rounds a price up to the nearest .10"""
	return (math.ceil(price*10))/10



"""DISPLAY FUNCTIONS"""

def show_holdings():
	for option in open_options.values():
		print(option)	


"""OBJECTS"""

class Portfolio:

	def __init__(self):
		self.buying_power = buying_power()

class Option:

	def __init__(self, info):
		"""info input is the dictionary obtained by calling current_option_positions()"""
		assert type(info) == dict
		self.info = info
		self.option_id = info['option_id']
		self.holder_id = info['id']
		self.instrument_data = instrument_data_by_id(self.option_id)
		self.type = self.instrument_data['type']
		self.symbol = self.instrument_data['chain_symbol']
		self.expiration_date = self.instrument_data['expiration_date']
		self.strike_price = self.instrument_data['strike_price']
		self.purchase_date = info['created_at'][:10]

		alter_shelve(open_options, 'add', self.holder_id, self)
	
	@property
	def market_data(self):
		return market_data_by_id(self.option_id)

	@property
	def average_cost(self):
		price = string_to_rounded(self.info['average_price'])
		return price

	@property
	def quantity(self):
		return int(eval(self.info['quantity']))
	
	@property
	def available_quantity(self):
		return int(float((self.info['quantity']))) - int(float((self.info['pending_sell_quantity'])))

	@property
	def mark_price(self):
		price = string_to_rounded(self.market_data['adjusted_mark_price'])
		return price

	@property
	def percent_change(self):
		unrounded = (self.mark_price*(100/self.quantity) - self.average_cost)*100/self.average_cost
		return round(unrounded, 2)


	def target_limit(self, target_percent):
		"""Calculates the limit price from a target"""
		return round_to_tenth((self.average_cost/100)*(1 + (target_percent/100)))

	def limit_sell_all(self, target_percent):

		limit_price = self.target_limit(target_percent)
		quantity = self.available_quantity
		sell_option(self, quantity, limit_price)


	def __repr__(self):

		return "{0}, type: {1}, strike: {2}, expiration: {3}, quantity: {4}, average cost: {5}, mark price: {6}, percent change: {7}%" \
				.format(self.symbol, self.type, self.strike_price, self.expiration_date, self.quantity, self.average_cost, self.mark_price, self.percent_change)

	def __str__(self):

		return "{0}, type: {1}, strike: {2}, expiration: {3}, quantity: {4}, average cost: {5}, mark price: {6}, percent change: {7}%" \
				.format(self.symbol, self.type, self.strike_price, self.expiration_date, self.quantity, self.average_cost, self.mark_price, self.percent_change)


class Buy:

	order_type = 'buy'
	position_effect = 'open'
	direction = 'debit'

	def __init__(self, symbol, option_type, expiration_date, strike_price, quantity, limit_price):
		assert option_type in ['call', 'put']
		assert type(expiration_date) == str and type(symbol) == str and type(strike_price) == str
		assert all(type(arg) in [float, int] for arg in [quantity, limit_price])

		self.quantity = quantity
		self.limit_price = limit_price
		self.strike_price = strike_price
		self.expiration_date = expiration_date
		self.option_type = option_type
		self.symbol = symbol
		robin_stocks.orders.order_buy_option_limit('open', 'debit', self.limit_price, self.symbol, self.quantity, self.expiration_date, self.strike_price, self.option_type, 'gtc')

	def __repr__(self):

		return 'Order placed to buy {0} {1}(s) of {2} expiring on {3} with a strike price of ${4} at a limit price of {5}.'.format(self.quantity, self.option_type, self.symbol, self.expiration_date, self.strike_price, self.limit_price)




class Sell:

	order_type = 'sell'
	position_effect = 'close'
	direction = 'credit'

	def __init__(self, symbol, option_type, expiration_date, strike_price, quantity, limit_price):
		"""Initiates a sell-to-close on a current option OBJECT."""
		assert type(limit_price) in [float, int]
		assert type(quantity) == int
		self.limit_price = limit_price
		self.strike_price = strike_price
		self.expiration_date = expiration_date
		self.option_type = option_type
		self.symbol = symbol
		self.quantity = quantity
		robin_stocks.orders.order_sell_option_limit('close', 'credit', self.limit_price, self.symbol, self.quantity, self.expiration_date, self.strike_price, self.option_type, 'gtc')
	
	def __repr__(self):

		return 'Order placed to sell {0} {1}(s) of {2} expiring on {3} with a strike price of ${4} at a limit price of {5}.'.format(self.quantity, self.option_type, self.symbol, self.expiration_date, self.strike_price, self.limit_price)


	
"""ROBIN STOCKS FUNCTIONS"""

"""PORTFOLIO"""

def load_financials():
	"""Returns portfolio"""
	return robin_stocks.profiles.build_user_profile()


def buying_power():
	financials = load_financials()
	return string_to_rounded(financials['cash'])

"""OPTIONS"""

def current_option_positions(info=None):
	"""Gives holding and option id data for open positions. INSTANT. No market or instrument data"""
	return robin_stocks.options.get_open_option_positions(info)

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
	return robin_stocks.options.get_option_instrument_data_by_id(option_id)

def chain_data(symbol, info=None):
	"""Gets chain data for stock. INSTANT. Includes possible expiration dates for options."""
	assert type(symbol) == str
	return robin_stocks.options.get_chains(symbol, info)

def get_list_of_strikes(symbol, expiration_date, option_type="call"):

	unordered_string = options_by_expiration(symbol, expiration_date, option_type, 'strike_price')
	floats = [float(price) for price in unordered_string]
	floats.sort(reverse=False)
	return [str(price) for price in floats]


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


"""DATETIME FUNCTIONS"""

def get_military_time():
	"""Returns the time in HHMM format"""
	time = datetime.now()
	return time.strftime("%H%M")

def string_to_date(std_date):
	"""Takes in a string date and converts it to a date form for computation."""
	year = int(std_date[0:4])
	month = int(std_date[5:7])
	day = int(std_date[8:])
	return date(year, month, day)

def date_to_string(date_object):
	"""Takes in a date object and returns it as a formatted date: YYYY-MM-DD"""
	return date_object.strftime("%Y-%m-%d")

def date_remove_dashes(std_date):
	"""STD_DATE is a date in string form with dashes. Removes dashes for storage in JSON."""
	return std_date[0:4] + std_date[5:7] + std_date[8:]

def date_add_dashes(no_dash):
	"""NO_DASH is a date string with no dashes. This function puts in dashes"""
	return no_dash[0:4] + "-" + no_dash[4:6] + '-' + no_dash[6:8]

def current_date():
	"""Returns current date in date form"""
	return date.today()

def current_year():

	today = date_to_string(current_date())
	return today[0:4]

def days_away(date):
	"""Takes in the string form of a date and returns the number of days until date."""

	mod_date = string_to_date(date)
	return abs((current_date() - mod_date).days)

def is_future(query_date):
	"""QUERY_DATE is a string-formatted date: "YYYY-MM-DD". Checks to see if date has passed."""
	today_date = date_remove_dashes(date_to_string(current_date()))
	query_date = date_remove_dashes(query_date)

	if int(today_date) - int(query_date) < 0:

		return True

	return False

def is_today(date):
	"""Takes in the string form of a date and returns whether or not that date is today."""
	date = string_to_date(date)
	if date == current_date():
		return True
	return False

def is_day_trade(option):
	"""Takes in an option object, and returns whether or not selling that option will be a day trade."""
	if is_today(option.purchase_date):
		return True

	return False










