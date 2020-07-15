from options import *
import json

from apscheduler.schedulers.blocking import BlockingScheduler

tracked_stocks = []

def read_json(filename):
	"""FILENAME is the name of a json file containing option information. This function loads the json object into the script 
	to be edited. The return object is the option dictionary to be edited."""

	data_file = open(filename, "r")
	data = json.load(data_file)
	data_file.close()

	return data

def dump_json(updated_dict, filename):
	"""UPDATED_DICT is the option object with updated data. FILENAME is the name of the json file containing the option information.
	Run this function to update json files with new option data."""
	data_file = open(filename, "w")
	json.dump(updated_dict, data_file)
	data_file.close()

	return "{0} successfully updated".format(filename)


def list_tracked_stocks():
	"""Returns a list of all stock symbols for the stocks being tracker"""
	data = read_json("tracked_stocks.json")
	return list(data.keys())


def setup_daily_info():

	for stock in list_tracked_stocks():
		tracked_stocks.append({'symbol':stock, 'date': date_to_string(date.today()), 'market_data': {}})
		JSON_file_name = stock + ".json"
		stock_data = read_json(JSON_file_name)


"""Gabe's Work"""






# def get_ids(shelf, symbol):

# 	stock_dict = shelf[symbol]
# 	put_dict, call_dict = stock_dict['call'], stock_dict['put']
# 	put_strikes = list(put_dict.keys())

# def option_tracker(symbol, expiration_date, strike, option_type):

# 	option_dict = all_options_data[expiration_date][symbol][option_type][strike]

# def get_options_six_away(symbol, )

# def day_info_storer(symbol) :

# 	"""For each strike of each expiration, find the market data"""



# def initialize(symbol)

# all_options_data = {

# 'SPY:' {

# 	'expiration date1' {


# 		'put': {

# 			'55': {

# 				'id': 

# 				'2021-07-09': {
# 					'630': "all market data"
# 					'1330'
# 				}
# 			}
# 			'50':
# 			'45':
# 			'40':

# 		}

# 		'call': {


# 		}

# 	}

# 	'SPXL': {

# 	}

# 	'TSLA': {

# 	}
	

# }

# """Sam's Work"""