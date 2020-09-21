import datetime as dt
from datetime import date, datetime


def utc_to_military(utc_time):
	"""Takes UTC time (HH-MM) and converts it to military time: (HHMM)"""
	utc_hour = utc_time[0:2]
	minute = utc_time[3:]

	hour = str(int(utc_hour) - 7)

	return hour + minute


def get_military_time():
	"""Returns the time in HHMM format"""
	time = datetime.now()
	return time.strftime("%H%M")

def time_between(time1, time2):

	return abs(int(time1) - int(time2))

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

def current_date_as_string():

	return date_to_string(current_date())

def get_year(date):
	"""Get year of DATE string"""
	return date[0:4]

def current_year():

	today = date_to_string(current_date())
	return today[0:4]

def days_between(start_date, end_date):
	return (string_to_date(end_date) - string_to_date(start_date)).days

def days_away(date):
	"""Takes in the string form of a date and returns the number of days until date."""

	mod_date = string_to_date(date)
	return abs((current_date() - mod_date).days)


def is_future(query_date, starting_date='today'):
	"""QUERY_DATE is a string-formatted date: "YYYY-MM-DD". Checks to see if query date is in the future."""
	if starting_date == 'today':

		starting_date = date_remove_dashes(date_to_string(current_date()))

	else:

		starting_date = date_remove_dashes(starting_date)

	query_date = date_remove_dashes(query_date)


	if int(starting_date) - int(query_date) < 0:

		return True

	return False

def is_not_past(query_date, starting_date='today'):
	"""QUERY_DATE is a string-formatted date: "YYYY-MM-DD". Return true if the query date is not in the past of the starting date.
	is_not_past("2020-08-07", "2020-08-01") --> true
	is_not_past("2020-08-07", "2020-09-01") --> false
	"""

	if starting_date == 'today':

		starting_date = date_remove_dashes(date_to_string(current_date()))

	else:

		starting_date = date_remove_dashes(starting_date)

	query_date = date_remove_dashes(query_date)

	if int(starting_date) - int(query_date) <= 0:

		return True

	return False

def is_in_range(query_date, start_date, end_date):

	if not end_date and not start_date:

		return True

	elif not start_date:

		return is_not_past(end_date, query_date)

	elif not end_date:

		return is_not_past(query_date, start_date)

	else:

		return is_not_past(query_date, start_date) and is_not_past(end_date, query_date)

def is_today(date):
	"""Takes in the string form of a date and returns whether or not that date is today."""
	date = string_to_date(date)
	if date == current_date():
		return True
	return False
