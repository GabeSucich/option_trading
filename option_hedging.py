from options import *

def choose_option_strikes(symbol, expiration_date, buying_power, sold_option):
	"""Chooses which options to purchase. Call and put strikes list"""

	calls_to_purchase = []
	puts_to_purchase = []
	call_num = 0
	put_num = 0
	switch = sold_option #The switch variable will control if we are looking to prioritize buying calls or puts

	def switcher():
		"""A helper function which helps to switch the purchasing priority."""
		nonlocal switch
		if switch == 'call':
			switch = 'put'
		else:
			switch = 'call'

	calls_and_puts = produce_pairings(symbol, expiration_date)
	call_strikes, put_strikes = calls_and_puts['call pairs'], calls_and_puts['put pairs']

	def option_searcher(call_strikes, put_strikes, buying_power, searches = 0, bought_call=False, bought_put=False):
		"""A helper function that will search through options and add them to cart"""
		nonlocal calls_to_purchase
		nonlocal puts_to_purchase
		nonlocal call_num
		nonlocal put_num

		closest_call, remaining_calls, closest_put, remaining_puts = call_strikes[-1], call_strikes[0:-1], put_strikes[0], put_strikes[1:]
		call_strike, call_price, put_strike, put_price = list(closest_call.keys())[0], list(closest_call.values())[0], list(closest_put.keys())[0], list(closest_put.values())[0]
		call_price, put_price = round_to_tenth(call_price), round_to_tenth(put_price)


		price_split = buy_splitter(call_price, put_price, buying_power, switch)

		if searches == 3:

			return

		elif switch == 'call':

			if price_split == 0:

				if bought_call and bought_put:

					return

				else:

					option_searcher(remaining_calls, put_strikes, buying_power, searches + 1, bought_call, bought_put)

			elif price_split == 1:

				option_searcher(remaining_calls, put_strikes, buying_power, searches + 1, bought_call, bought_put)

			elif price_split[1] == 0:

				switcher() #Changes the priority to buying a put
				call_quantity, new_buying_power = price_split[0], price_split[2]
				calls_to_purchase.append({'symbol': symbol, 'expiration_date': expiration_date, 'strike_price': call_strike, 'price': call_price, 'quantity': call_quantity, 'type': 'call'})
				option_searcher(remaining_calls, remaining_puts, new_buying_power, searches + 1, True, bought_put)

			else:

				if price_split[0] > price_split[1]:
					switcher() #Changes priority if more calls were bought than puts

				call_quantity, put_quantity, new_buying_power = price_split[0], price_split[1], price_split[2]
				calls_to_purchase.append({'symbol': symbol, 'expiration_date': expiration_date, 'strike_price': call_strike, 'price': call_price, 'quantity': call_quantity, 'type':'call'})
				puts_to_purchase.append({'symbol': symbol, 'expiration_date': expiration_date, 'strike_price': put_strike, 'price': put_price, 'quantity': put_quantity, 'type':'put'})

				option_searcher(remaining_calls, remaining_puts, new_buying_power, searches + 1, True, True)

		elif switch == 'put':

			if price_split == 0:

				if bought_call and bought_put:

					return

				else:

					option_searcher(call_strikes, remaining_puts, buying_power, searches + 1, bought_call, bought_call)

			elif price_split == 2:

				option_searcher(call_strikes, remaining_puts, buying_power, searches + 1, bought_call, bought_call)

			elif price_split[0] == 0:

				switcher() #Changes the priority to buying a put
				put_quantity, new_buying_power = price_split[1], price_split[2]
				puts_to_purchase.append({'symbol': symbol, 'expiration_date': expiration_date, 'strike_price': put_strike, 'price': put_price, 'quantity': put_quantity, 'type': 'put'})
				option_searcher(remaining_calls, remaining_puts, new_buying_power, searches + 1, bought_call, True)

			else:

				if price_split[0] < price_split[1]:
					switcher() #Changes priority if more puts were bought than calls

				call_quantity, put_quantity, new_buying_power = price_split[0], price_split[1], price_split[2]
				calls_to_purchase.append({'symbol': symbol, 'expiration_date': expiration_date, 'strike_price': call_strike, 'price': call_price, 'quantity': call_quantity, 'type':'call'})
				puts_to_purchase.append({'symbol': symbol, 'expiration_date': expiration_date, 'strike_price': put_strike, 'price': put_price, 'quantity': put_quantity, 'type':'put'})

				option_searcher(remaining_calls, remaining_puts, new_buying_power, searches + 1, True, True)

	strike_data = produce_pairings(symbol, expiration_date)
	call_strikes = strike_data['call pairs']
	put_strikes = strike_data['put pairs']

	option_searcher(call_strikes, put_strikes, buying_power)

	return calls_to_purchase + puts_to_purchase


def split_generator(price1, price2, buy_power):
		"""Yields all possible combinations with: [number of price1 options, number of price2 options, unused buying power]"""

		price1 *= 100
		price2 *= 100

		max_price1_num = buy_power//price1

		for price1_num in (range(int(max_price1_num + 1))):
			price2_num = int((buy_power - price1_num*price1)//price2)
			leftover = buy_power - price1_num*price1 - price2_num*price2
			yield [price1_num, price2_num, leftover]
			

def buy_splitter(call_price, put_price, buy_power, sold_option):
	"""Takes in two option prices and a buying power. Returns the 
	desired way to split buying power between new call and put: [number of calls, number of puts]."""
	assert sold_option in ['call', 'put']

	possible_splits = list(split_generator(call_price, put_price, buy_power))

	if len(possible_splits) == 1 and possible_splits[0][0] == 0 and possible_splits[0][1] == 0:

		return 0

	def call_put_difference(split):
		"""Helper function that returns the number of call options minus the number of put options for a given split."""
		return split[0] - split[1]

	if all([(split[0] == 0 or split[1] == 0) for split in possible_splits]):
		"""Will deal with the case that only one option can be bought. If a put was previously bought and only a call can be afforder, or vice versa,
		then None will be returned. Else, the normal return value will be given"""

		only_calls = [split for split in possible_splits if split[0] != 0]
		only_puts = [split for split in possible_splits if split[1] != 0]

		if (sold_option == 'call' and len(only_calls) == 0):

			return 1


		elif (sold_option == 'put' and len(only_puts) == 0):

			return 2

		elif sold_option == 'call':

			return only_calls[0]

		else:

			return only_puts[0]

	else: 

		if sold_option == 'call':

			return min([split for split in possible_splits if call_put_difference(split) >= 0], key=call_put_difference)

		else:

			return min([split for split in possible_splits if call_put_difference(split) <= 0], key=(lambda x: - call_put_difference(x)))

def pair_strikes_and_prices(symbol, strike_list, expiration_date, option_type):
	"""Returns a dictionary of strike prices and option costs for the given strike list taken in. 
	The strike_list argument is a list of floates. In the returned list, keys are strings and values are floats."""
	assert option_type in ['call', 'put']

	strike_price_pair = []

	for strike_price in strike_list:

		str_strike_price = str(strike_price)
		option_price_list = options_by_expiration_and_strike(symbol, expiration_date, str_strike_price, option_type, 'adjusted_mark_price')
		option_price = float(option_price_list[0])
		strike_price_pair.append({str_strike_price : option_price})

	return strike_price_pair

def produce_pairings(symbol, expiration_date):
	"""Returns a dictionary of call pairs and put pairs. Each value is a list of dictionaries. The keys are string strike prices,
	and the values are float mark prices."""

	strike_list = get_list_of_strikes(symbol, expiration_date)
	call_put_strikes = strike_splitter(latest_stock_price(symbol), strike_list)
	call_pairs = pair_strikes_and_prices(symbol, call_put_strikes['call strikes'], expiration_date, 'call')
	put_pairs = pair_strikes_and_prices(symbol, call_put_strikes['put strikes'], expiration_date, 'put')

	return {'call pairs' : call_pairs, 'put pairs': put_pairs}


def strike_splitter(share_price, strike_list):
	"""Takes in a share price, a list of strikes as strings. Returns higher prices for calls, and lower prices for puts."""


	price_list = [string_to_rounded(price) for price in strike_list]
	price_list.sort(reverse=True)
	larger_strikes = [strike for strike in price_list if strike >= share_price]
	smaller_strikes = [strike for strike in price_list if strike <= share_price]
	

	return {'call strikes': larger_strikes, 'put strikes': smaller_strikes}





			

