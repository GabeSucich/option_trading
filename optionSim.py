from optionhistoricals import *
from stocks import *
# CLASSES #

def printer(x, y, z, portfolio, stock, date, time, historicals):
	
	print('date:', date, "  time:", time)
	return []


class Simulation:

	def __init__(self, symbol, investment, strategy_function, fixed_parameters, start_date, end_date, time_step="30minutes"):

		self.strategy = strategy_function
		self.fixed_parameters = fixed_parameters
		self.calendar = SimCalendar(start_date, end_date, time_step)
		self.stock_sim = SimStock(symbol, start_date, end_date)
		self.historicals = get_json_object(symbol)
		self.portfolio = Portfolio(investment)
		self.finished = False

	def run_simulation(self):

		while not self.finished:

			self.simulate_next_data_point()

	def get_next(self):

		return self.calendar.next_test_point()

	def simulate_next_data_point(self):

		data_point = self.get_next()

		if not data_point:

			self.finished = True
			return

		date, time = data_point['date'], data_point["time"]

		self.portfolio.update_holdings(date, time)

		suggestions = self.strategy(*self.fixed_parameters, portfolio=self.portfolio, stock=self.stock_sim, date=date, time=time, historicals=self.historicals)

		self.handle_suggestions(suggestions)



	def handle_suggestions(self, suggestions):

		sells, buys = [],[]

		for suggestion in suggestions:
			if suggestion['action'] == 'sell':
				sells.append(suggestion)
			else:
				buys.append(suggestion)

		for suggestion in sells:

			self.process_sell(suggestion)

		for suggestion in buys:

			self.process_buy(suggestion)



	def process_buy(self, suggestion):

		expiration_date, strike_price, option_type, quantity, cost = suggestion['expiration_date'], format_strike_price(suggestion['strike_price']), suggestion['option_type'], suggestion['quantity'], suggestion['cost']
		historicals = self.historical[expiration_date][option_type + 's'][strike_price]

		new_option = Option(self.symbol, expiration_date, strike_price, option_type, quantity, cost, historicals)

		self.portfolio.buy_option(new_option)

	def process_sell(self, suggestion):

		option = suggestion['option'],
		quantity = suggestion['quantity']
		sell_price = suggestion['sell_price']
		self.portfolio.sell_option(option, quantity, sell_price)


class SimCalendar:

	def __init__(self, start_date, end_date, time_step="30minutes"):

		self.dates = get_all_market_dates(start_date, end_date)
		self.time_step = time_step
		self.timeline = self.produce_timeline()
		self.current_day = next(self.timeline)

	def next_test_point(self):

		next_time = self.current_day['daySim'].next_time()

		if not next_time:

			self.next_day()

			if not self.current_day:

				print('Simulation finished!')
				return None

			next_time = self.current_day['daySim'].next_time()

		return {"date": self.current_day['date'], "time": next_time}

				
	def produce_timeline(self):

		for date in self.dates:

			yield {'date': date, 'daySim': SimDay(date, self.time_step)}

	def next_day(self):

		self.current_day = next(self.timeline, None)


class SimDay(SimCalendar):

	def __init__(self, date, time_step):

		self.date = date
		assert time_step in ["30minutes", "hour", "2hours", "day"], "Invalid time step"
		self.time_step = time_step
		self.timeline = self.produce_hourly_timeline()

	def produce_hourly_timeline(self):

		for hour in get_hours_in_day(self.time_step):

			yield hour

	def next_time(self):

		return next(self.timeline, None)


class Portfolio:

	def __init__(self, investment, options=[]):
		self.initial_value = investment
		self.buying_power = investment
		self.invested = 0
		self.options = []
		self.history = []

	@property
	def total_value(self):
		return self.buying_power + self.invested

	def update_holdings(self, date, time):

		for option in self.options:

			option.update_price(date, time)

		self.update_value_from_holdings()
		self.add_historical_data(date, time)


	def update_value_from_holdings(self):

		self.invested = 0
		for option in self.options:

			self.invested += option.open_price*option.quantity

	def add_historical_data(self, date, time):

		current_value = self.total_value
		data_point = {'date': date, 'time':time, 'portfolio_value':current_value}
		self.history.append(data_point)

	def buy_option(self, option):

		self.options.append(option)
		if self.buying_power < option.total_cost:
			print("Not enough buying power to purchase", option)
		else:
			self.invested += option.total_cost
			self.buying_power -= option.total_cost

	def sell_option(self, option, quantity, sell_price):

		if quantity > option.quantity:

			print(quantity, "options of", option, "are not owned")

		else:
			self.option -= quantity

			if self.option.quantity == 0:

				self.options.remove(option)

			profit = quantity*sell_price

			self.invested -= profit
			self.buying_power += profit


class Option:

	def __init__(self, symbol, expiration_date, strike_price, option_type, quantity, average_cost, historicals):
		self.symbol = symbol
		self.expiration_date = expiration_date
		self.strike_price = format_strike_price(strike_price)
		self.option_type = option_type
		self.quantity = quantity
		self.average_cost = average_cost
		self.historicals = historicals
		self.current_price_info = {}

	def __repr__(self):

		return "${0} {1} for {2} expiring on {3}. Percent change: %{4}".format(self.strike_price, self.option_type, self.symbol, self.expiration_date, self.percent_change)

	def __str__(self):

		"${0} {1} for {2} expiring on {3}".format(self.strike_price, self.option_type, self.symbol, self.expiration_date)
	@property
	def total_cost(self):
		return self.average_cost*self.quantity

	@property
	def percent_change(self):
		return round((self.current_price - self.cost)*100/self.cost, 2)

	@property
	def raw_change(self):
		return self.quantity*(self.current_price - self.cost)

	@property
	def high_price(self):
		return float(self.current_price["high_price"])*100

	@property
	def low_price(self):
		return float(self.current_price["low_price"])*100

	@property
	def open_price(self):
		return float(self.current_price["open_price"])*100

	@property
	def close_price(self):
		return float(self.current_price["close_price"])*100
	
	def update_price(self, date, time):
		self.current_price_info = self.historicals[date][time]
	

class SimStock:

	def __init__(self, symbol, start_date, end_date):
		self.symbol = symbol
		self.start_date = start_date
		self.end_date = end_date
		self.sim_length = self.get_historicals_span()
		self.historicals = self.get_best_historicals()

	def get_historicals_span(self):

		return days_between(self.start_date, self.end_date)

	def get_best_historicals(self):

		if self.sim_length == 1:
			all_historicals = get_stock_historicals(self.symbol, '5minute', 'day')
		elif self.sim_length <= 7:
			all_historicals = get_stock_historicals(self.symbol, '10minute', 'week')
		elif self.sim_length <= 30:
			all_historicals = get_stock_historicals(self.symbol, 'hour', 'month')
		elif self.sim_length <= 90:
			all_historicals = get_stock_historicals(self.symbol, 'hour', '3month')
		elif self.sim_length <= 365:
			all_historicals = get_stock_historicals(self.symbol, 'day', 'year')
		else:
			all_historicals = get_stock_historicals(self.symbol, 'week', '5year')

		return stock_historicals_between_dates(all_historicals, self.start_date, self.end_date)

	def get_closest_match(self, date, time):

		closest_date = get_closest_date(self.historicals, date)

		closest_data_points = [data_point for data_point in self.historicals if get_historical_date(data_point) == closest_date]

		if len(closest_data_points) == 1:

			return closest_data_points[0]

		else:

			closest_time = get_closest_time(closest_data_points, time)
			closest_data_point = [data_point for data_point in closest_data_points if utc_to_military(get_historical_time(data_point)) == closest_time]
			return closest_data_point[0]

# ---------------------------------------------------------------------------------------------#

# HELPER FUNCTIONS

def get_closest_date(historicals, date):

	closest_date = None
	closest_distance = 0
	for data_point in historicals:

		history_date = get_historical_date(data_point)
		days_away = abs(days_between(date, history_date))

		if (not closest_date) or days_away < closest_distance:

			closest_date = history_date
			closest_distance = days_away

	return closest_date

def get_closest_time(day_history, time):

	closest_time = None
	closest_distance = 0

	for data_point in day_history:

		history_time = utc_to_military(get_historical_time(data_point))
		minutes_away = time_between(time, history_time)

		if not closest_time or minutes_away < closest_distance:

			closest_time = history_time
			closest_distance = minutes_away


	return closest_time


def get_all_market_dates(start_date, end_date):

	market_dates = []

	start_year = int(get_year(start_date))
	end_year = int(get_year(end_date))
	year_range = range(start_year, end_year + 1)

	date_to_check = start_date

	holidays = get_holiday_dates(years = [year for year in year_range])

	while is_not_past(end_date, starting_date=date_to_check):

		date_object = string_to_date(date_to_check)
		day_of_week = date_object.weekday()
		
		if day_of_week < 5 and date_to_check not in holidays:

			market_dates.append(date_to_check)
		
		date_object += dt.timedelta(days=1)
		date_to_check = date_to_string(date_object)

	return market_dates

def get_hours_in_day(time_step):

	if time_step == "30minutes":

		return ["630", "700", "730", "800", "830", "900", "930", "1000", "1030", "1100", "1130", "1200", "1230"]

	elif time_step == "hour":

		return ["630", "730", "830", "930", "1030", "1130", "1230"]

	elif time_step == "2hours":

		return ["630", "830", "1030", "1230"]

	else:

		return ["1000"]



