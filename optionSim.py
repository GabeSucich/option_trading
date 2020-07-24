import options
import optionhistoricals

class Simulation:

	def __init__(self, initial_value, stock_symbol, strategy_function, positional_arguments, start_date, end_date):



		self.stored_data = []

		self.json_data = get_json_object(stock_symbol)

		self.date = start_date
		self.options = []
		self.portfolio = Portfolio(initial_value)
		self.invested = 0

	def get_all_valid_dates():



	def store_data(self):
		self.stored_data.append(self.portfolio.value)

	def display_portfolio(self):

		print(self.portfolio_value())

	def display_profit(self):
		print(self.portfolio.profit)

	def next_period(self):
		###do something to update current_date of simulation
		for option in self.options:
			option.update(date)

		self.run_period(self.date)

	def run_period(self, date):

		suggestions = self.strategy_function(*positional_arguments, options=self.options)
		self.Process(suggestions)
		self.next_period()





class Porfolio:

	def __init__(self, initial_value):

		self.options = []
		self.initial_investment = initial_value
		self.value = initial_value
		self.invested = 0

	@property
	def buying_power(self):
		return self.value - self.invested

	@property
	def profit(self):
		return portfolio_value - self.initial_investment
	

	def purchase_option(self, option):
		self.add_option(option)

	def add_option(self, option):
		self.options.append(option)
		self.invested += option.price


class SimOption:

	pass

class SimCall(SimOPtion):
		
	def get_day(json_data, date):

		return json_data[expiration_date][option_type + 's'][strike_price][date]

class SimPut(SimOption):

	option_type = "put"

	def __init__(self, expiration_date, strike_price, quantity, average_price):


class SimDay:

	def __init__(self, json_data)


def simulation():

	while true:

		Do stuff
