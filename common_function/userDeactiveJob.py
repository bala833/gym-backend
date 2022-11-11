from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .job import schedule_api, myjob


def start():
	scheduler = BackgroundScheduler()
	# scheduler.add_job(schedule_api, 'interval', minutes=1) #schedule_api comming from job.py file
	# scheduler.add_job(myjob, 'interval', seconds=1)
	scheduler.start()