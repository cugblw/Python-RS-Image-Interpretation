from datetime import datetime
from datetime import date
import time
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

text = 0
def test_job(text):
    print(text+1)

def test_job2(text):
    print(text+2)


def main():
    scheduler = BlockingScheduler(timezone = 'UTC')
    scheduler.add_job(test_job, 'interval', seconds=3, args=[text])
    scheduler.add_job(test_job2, 'interval', seconds=3, args=[text])
    scheduler.start()

if __name__=='__main__':
    main()