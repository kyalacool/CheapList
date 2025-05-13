import datetime
import os
import sys

from dotenv import load_dotenv

from database import DbManager

load_dotenv()

ALL_MAINTYPE = {'egg': os.environ.get('EGG_URL'), 'milk_2_8' : os.environ.get('MILK_2_8_URL'), 'cheese':os.environ.get('CHEESE_URL'), 'chicken_meat' : os.environ.get('CHICKEN_MEAT_URL'), 'sea_fish' : os.environ.get('SEA_FISH')}
db = DbManager()
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

if __name__ == '__main__':
    main()