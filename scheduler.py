from optionhistoricals import *
from apscheduler.schedulers.background import BackgroundScheduler

# from apscheduler.schedulers.blocking import BlockingScheduler

"""Initialize the blocking scheduler"""
option_scheduler = BackgroundScheduler()

"""JOBS"""

option_scheduler.add_job(setup_daily_info, "cron", day_of_week="mon-fri", hour="6")

option_scheduler.add_job(update_all_data, "cron", day_of_week="mon-fri", hour="7-12", minute="0, 30")

option_scheduler.add_job(update_all_data, "cron", day_of_week="mon-fri", hour="6", minute="30", second="2")

option_scheduler.add_job(update_all_data, "cron", day_of_week="mon-fri", hour="13", minute="0")

option_scheduler.add_job(update_all_json, "cron", day_of_week="mon-fri", hour="14", minute="0")

option_scheduler.add_job(clear_daily_info, "cron", day_of_week="mon-fri", hour="17", minute="0")

option_scheduler.add_job(update_expirations_for_all, "cron", day_of_week="sun", hour="12", minute="0")

option_scheduler.start()
