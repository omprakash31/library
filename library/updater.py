from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
def tick():
    print('One tick!')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=10)
    # scheduler.add_job(tick, 'interval', minutes=5)
    scheduler.start()