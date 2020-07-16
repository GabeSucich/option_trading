from optionhistoricals import *

from apscheduler.schedulers.blocking import BlockingScheduler

"""Initialize the blocking scheduler"""
option_scheduler = BlockingScheduler()

"""JOBS"""

option_scheduler.add_job(setup_daily_info)

option_scheduler.add_job(update_all_data)

option_scheduler.add_job(update_all_json)

option_scheduler.add_job(clear_daily_info)
