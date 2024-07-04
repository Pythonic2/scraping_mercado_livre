import schedule
import time
import pytz
from scrap import Bot_chrome
def job():
    bot = Bot_chrome()
    print("I'm working...")
    print(time.strftime("%H:%M:%S"))
    bot.acessar()

schedule.every(60).seconds.do(job)

    
while True:
    schedule.run_pending()
