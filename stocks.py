import shelve
import robin_stocks
import time
import atexit

robin_stocks.login('gabe.sucich@gmail.com', 'Chicag0I11inoi$99')


def show_active_orders():
	if not Order.active_orders:
		print('No active orders')
	for orderID in Order.active_orders.keys():
		order = Order.active_orders[orderID]
		print(order, '\n')

def show_holdings():
	for stock in Holdings.holdings.keys():
		print(Holdings.holdings[stock].__repr__() + '\n')

def shelve_closer():
	Holdings.holdings.close()
	Order.active_orders.close()
	Update.pairings.close()

atexit.register(shelve_closer)

def update_from_robinhood():

	Update.update_from_robinhood()
	show_holdings()
	show_active_orders()

def update_orders():

	Order.update_orders()


class Holdings:

	holdings = shelve.open('holdings', writeback=True)

	def stock_owned(symbol):
		"""Returns True of stock is in holdings, and False otherwise"""
		if symbol in holdings.keys():
			return True
		else:
			return False

	def order_response(stock_symbol):
		if stock_symbol in Holdings.holdings.keys():
			return Holdings.holdings[stock_symbol]
		else:
			return Stock(stock_symbol)

	def robinhood_update(stock_list):
		#takes in a dicionary of stocks after update from robinhood initiated
		for stock in stock_list.keys():
			symbol = stock
			info = stock_list[symbol]
			price = round(eval(info['price']), 2)
			shares = round(eval(info['quantity']), 2)
			average_buy_cost = round(eval(info['average_buy_price']), 2)
			Stock(symbol, shares, average_buy_cost)

	def get_stock_object_from_symbol(symbol):
		if symbol not in Holdings.holdings.keys():
			return 'No shares of {0} are owned'.format(symbol)
		else:
			return Holdings.holdings[symbol]


class Stock(Holdings):

	def __init__(self, symbol, shares=0, average_buy_cost=0):
		self.symbol = symbol
		self.name = Update_Stock.name_from_symbol(symbol)
		self.shares = shares
		self.average_buy_cost = average_buy_cost
		self.pending_sales = 0
		self.pending_buys = 0
		Holdings.holdings[self.symbol] = self
		Holdings.holdings.sync()

	def __repr__(self):

		return '{0} ({1}): current_price: {2}, shares: {3}, pending_sales: {4}, pending_buys: {5}, average_buy_cost" {6}, profit: {7}, percent_change: {8}'.format(self.name, self.symbol, self.price, self.shares, self.pending_sales, self.pending_buys, self.average_buy_cost, self.profit, self.percent_change)

	@property
	def equity(self):
		return self.price*self.shares

	@property
	def price(self):
		return Update_Stock.latest_price(self.symbol)
	

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
	
	

	

	def remove_stock(self):
		"""Removes a stock that has been completely sold from dictionary"""
		assert self.shares == 0
		del Holdings.holdings[self.symbol]
		Holdings.holdings.sync() 


	def new_order_stock_update(self, order):
		"""Updates a stock in the holding after a new order and pairing have created"""

		if order.side == 'sell':

			assert order.shares <= self.available_shares
			self.pending_sales += order.shares

		elif order.side == 'buy':

			self.pending_buys = order.shares

		Holdings.holdings.sync()

	def current_order_stock_update(self, order):
		"""Updates stock when orders are updated from Robinhood"""

		
		if order.side == 'sell':

			if order.completeness() == 'complete':


				self.shares -= self.pending_sales
				self.pending_sales = 0
				

			elif order.completeness() == 'failed':

				self.pending_sales = 0




		else:

			if order.completeness() == 'complete':

				self.average_buy_cost = (self.shares*self.average_buy_cost + order.shares*order.info['average_price'])/(self.shares + order.shares)
				self.shares += self.pending_buys
				self.pending_buys = 0

			elif order.completeness() == 'failed':

				self.pending_buys = 0

				if self.shares == 0:
					self.remove_stock()

		Holdings.holdings.sync()



class Order:

	active_orders = shelve.open('orders', writeback=True)
	"""Dictionary where the keys are order IDs and the values are order objects"""

	complete_states = ['filled', 'cancelled', 'failed', 'uncomfirmed']
	successful_states = ['filled']
	failed_states = ['failed', 'cancelled', 'unconfirmed']
	pending_states = ['queued', 'pending', 'confirmed']

	trigger = 'immediate'
	limitPrice = None
	stopPrice = None
	timeInForce = 'gfd'
	extendedHours = True

	def robinhood_response(orders):
		"""When all stock/order info is initially loaded into program from Robinhood, adds orders to active_orders and
		creates pairing with associated stock objects"""
		for order in orders:
			
			Order.initiate_new_order(order)

	def add_order(self):
		"""Adds order object to dictionary"""
		orderID = self.info['id']
		self.active_orders[orderID] = self
		Order.active_orders.sync()

	def erase_order(orderID):
		del Order.active_orders[orderID]
		Order.active_orders.sync()


	def update_orders():
		"""Calls to Update class for Robinhood orders."""
		Order.refresh_orders()
		active_orders = Update.get_open_stock_orders()
		for active_order in active_orders:
			if active_order['id'] not in Order.active_orders.keys():
				Order.initiate_new_order(active_order)


		Order.active_orders.sync()
		Update.pairings.sync()



		
	def refresh_order(orderID):

		order = Update.order_lookup(orderID)
		Order.active_orders[orderID].info = order
		new_order_object = Order.active_orders[orderID]

		Order.active_orders.sync()
		Update.update_pairing(orderID, new_order_object)

		
	def refresh_orders():
		"""Looks up orders in dictionary to update"""
		for orderID in Order.active_orders.keys():
			Order.refresh_order(orderID)

	def cancel_order(orderID):

		robin_stocks.orders.cancel_stock_order(orderID)
		time.sleep(3)
		Order.refresh_order(orderID)


		Order.active_orders.sync()

	def cancel_all_orders():
		for orderID in Order.active_orders.keys():
			Order.cancel_order(orderID)

	def initiate_new_order(order):
		"""Initiatializes a new order"""
		symbol = Update.get_order_symbol(order)
		shares = round(eval(order['quantity']), 2)

		if order['side'] == 'sell':

			if order['type'] == 'limit' and order['trigger'] == 'immediate':
				limitPrice = eval(order['price'])
				limit_sell(symbol, shares, limitPrice, 1, order)
			elif order['type'] == 'market' and order['trigger'] == 'stop':
				stopPrice = eval(order['stop_price'])
				stop_loss_sell(symbol, shares, stopPrice, 1, order)
			elif order['type'] == 'market' and order['trigger'] == 'immediate':
				market_sell(symbol, shares, 1, order)

		else:

			if order['type'] == 'limit' and order['trigger'] == 'immediate':
				limitPrice = eval(order['price'])
				limit_buy(symbol, shares, limitPrice, 1, order)
			elif order['type'] == 'market' and order['trigger'] == 'stop':
				stopPrice = eval(order['stop_price'])
				stop_loss_buy(symbol, shares, stopPrice, 1, order)
			elif order['type'] == 'market' and order['trigger'] == 'immediate':
				market_buy(symbol, shares, 1, order)





	def execute(self):
		"""Executes order and initiates sell-stock object pairing active_order and """

		return Update.send_order(self.symbol, self.shares, self.order_type, self.trigger, self.side, self.limitPrice, self.stopPrice, self.timeInForce, self.extendedHours)

	def __init__(self):
		if self.robin == 0:
			self.info = self.execute() #executes order and binds returned dictionary to self.info
		self.orderID = self.info['id'] 
		self.add_order() #adds order to order dictionary
		Update.create_pairing(self, self.symbol) #creates pairing between order and stock
		time.sleep(5)
		Order.refresh_order(self.orderID)


	def __repr__(self):

		return """id: {0}, symbol: {1}, side: {2}, order_type: {3}, trigger: {4}, limitPrice: {5} stopPrice: {6}""".format(self.orderID, self.symbol, self.side, self.order_type, self.trigger, self.limitPrice, self.stopPrice)


	def completeness(self):

		state = self.info['state']

		if state in self.successful_states:
			return 'complete'

		elif state in self.failed_states:
			return 'failed'

		elif state in self.pending_states:
			return 'still processing'

		else:
			raise ValueError('Stock could not be updated because of unknown order state: {0}'.format(state))



class Sell(Order):

	side = 'sell'

class limit_sell(Sell):

	order_type = 'limit'

	def __init__(self, symbol, shares, limitPrice, robin=0, info=None):
		self.robin = robin
		if self.robin == 1:
			self.info = info
		self.symbol = symbol
		self.shares = shares
		self.limitPrice = limitPrice
		Order.__init__(self)

class market_sell(Sell):

	order_type = 'market'

	def __init__(self, symbol, shares, robin=0, info=None):
		self.robin = robin
		if self.robin == 1:
			self.info = info
		self.symbol = symbol
		self.shares = shares
		Order.__init__(self)

class stop_loss_sell(Sell):

	order_type = 'market'
	trigger = 'stop'

	def __init__(self, symbol, shares, stopPrice, robin=0, info=None):
		self.robin = robin
		if self.robin == 1:
			self.info = info
		self.symbol = symbol
		self.shares = shares
		self.stopPrice = stopPrice

		Order.__init__(self)


class Buy(Order):

	side = 'buy'

class limit_buy(Buy):

	order_type = 'limit'

	def __init__(self, symbol, shares, limitPrice, robin=0, info=None):
		self.robin = robin
		if self.robin == 1:
			self.info = info
		self.symbol = symbol
		self.shares = shares
		self.limitPrice = limitPrice
		Order.__init__(self)

class market_buy(Buy):

	order_type = 'market'

	def __init__(self, symbol, shares, robin=0, info=None):
		self.robin = robin
		if self.robin == 1:
			self.info = info
		self.symbol = symbol
		self.shares = shares
		Order.__init__(self)

class stop_loss_buy(Buy):

	order_type = 'market'
	trigger = 'stop'

	def __init__(self, symbol, shares, stopPrice, robin=0, info=None):
		self.robin = robin
		if self.robin == 1:
			self.info = info
		self.symbol = symbol
		self.shares = shares
		self.stopPrice = stopPrice

		Order.__init__(self)



class Update:

	pairings = shelve.open('pairings', writeback=True)

	complete_list = ['filled', 'cancelled', 'failed', 'uncomfirmed']

	def send_order(symbol, quantity, orderType, trigger, side, limitPrice, stopPrice, timeinforce, extendedHours):

		return robin_stocks.orders.order(symbol, quantity, orderType, trigger, side, limitPrice, stopPrice, timeinforce, extendedHours)

	def get_open_stock_orders():
		"""Returns a list of dictionaries for each open order"""
		return robin_stocks.orders.get_all_open_stock_orders()

	def get_stock_holdings():
		"""Returns a dictionary of stocks where each value is a dictionary of info for its key symbol"""
		return robin_stocks.account.build_holdings()

	def add_pairing(self):

		Update.pairings[self.order.orderID] = self
		Update.pairings.sync()

	def update_from_robinhood():
		"""Calls information from Robinhood, and overwrites dictionaries"""

		Update.pairings.clear()
		Holdings.holdings.clear()
		Order.active_orders.clear()
		stocks = Update.get_stock_holdings()
		#a DICTIONARY of stocks. 
		#Keys are symbols. Values are dictionaries of holding information
		orders = Update.get_open_stock_orders()
		#returns a LIST of dictionaries, one for each order
		Holdings.robinhood_update(stocks)
		Order.robinhood_response(orders)


	def order_lookup(orderID):
		return robin_stocks.orders.get_stock_order_info(orderID)



	def get_order_symbol(info):
		#takes in dictionary returned by order and returns associated stock symbol
		instrument_URL = info['instrument']
		instrument = robin_stocks.stocks.get_instrument_by_url(instrument_URL)
		symbol = instrument['symbol']
		return symbol


	def create_pairing(order, stock_symbol):
		Holdings.order_response(stock_symbol) #returns stock if it already is owner or initiates new stock in holdings
		pairing = Pairing(order, stock_symbol)
		pairing.add_pairing()
		Update.pairings.sync()


	def update_pairing(orderID, order):

		Update.pairings.sync()
		pairing = Update.pairings[orderID]
		pairing.order = order
		stock = Stock.get_stock_object_from_symbol(pairing.symbol)
		stock.current_order_stock_update(order)
		if order.completeness() == 'complete' or order.completeness() == 'failed':
			Order.erase_order(order.orderID)
			Update.erase_pairing(order.orderID)

		Update.pairings.sync()


	def erase_pairing(orderID):
		del Update.pairings[orderID]
		Update.pairings.sync()

class Pairing(Update):

	def __init__(self, order, symbol):
		self.order = order
		self.symbol = symbol
		Stock.get_stock_object_from_symbol(self.symbol).new_order_stock_update(self.order)
		self.add_pairing()

		

class Update_Stock(Update):

	def latest_price(symbol):
		price_list = robin_stocks.stocks.get_latest_price(symbol)
		price = price_list[0]
		return round(eval(price), 2)

	def name_from_symbol(symbol):
		return robin_stocks.stocks.get_name_by_symbol(symbol)




		


	

	








