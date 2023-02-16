from RovControl import RovController
from configparser import ConfigParser
from time import sleep
import threading


PATH_CONFIG = '/Users/yarik/Documents/SoftProteus/0.1/controll-post/'

config = ConfigParser()
config.read(PATH_CONFIG + 'config_pult.ini')

joi = RovController(config)

ThreadJoi = threading.Thread(target=joi.listen)
ThreadJoi.start()
while True:
    print(joi.DataPult)
    sleep(0.25)
