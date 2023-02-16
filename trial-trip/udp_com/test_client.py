import socket
import logging
import coloredlogs
from datetime import datetime  # получение  времени
from time import sleep  # сон
from ast import literal_eval  # модуль для перевода строки в словарик
from configparser import ConfigParser

DEBUG = False


class MedaLogging:
    '''Класс отвечающий за логирование. Логи пишуться в файл, так же выводться в консоль'''

    def __init__(self):
        self.mylogs = logging.getLogger(__name__)
        self.mylogs.setLevel(logging.DEBUG)
        # обработчик записи в лог-файл
        name = '-'.join('-'.join('-'.join(str(datetime.now()).split()).split('.')).split(':')) + '.log'

        self.file = logging.FileHandler(name)
        self.fileformat = logging.Formatter(
            "%(asctime)s:%(levelname)s:%(message)s")
        self.file.setLevel(logging.DEBUG)
        self.file.setFormatter(self.fileformat)
        # обработчик вывода в консоль лог файла
        self.stream = logging.StreamHandler()
        self.streamformat = logging.Formatter(
            "%(levelname)s:%(module)s:%(message)s")
        self.stream.setLevel(logging.DEBUG)
        self.stream.setFormatter(self.streamformat)
        # инициализация обработчиков
        self.mylogs.addHandler(self.file)
        self.mylogs.addHandler(self.stream)
        coloredlogs.install(level=logging.DEBUG, logger=self.mylogs,
        fmt='%(asctime)s [%(levelname)s] - %(message)s')

        self.mylogs.info('start-logging')

    def debug(self, message):
        '''сообщения отладочного уровня'''
        self.mylogs.debug(message)

    def info(self, message):
        '''сообщения информационного уровня'''
        self.mylogs.info(message)

    def warning(self, message):
        '''не критичные ошибки'''
        self.mylogs.warning(message)

    def critical(self, message):
        '''мы почти тонем'''
        self.mylogs.critical(message)

    def error(self, message):
        '''ребята я сваливаю ща рванет !!!!'''
        self.mylogs.error(message)



class ROVProteusClient:
    #Класс ответсвенный за связь с постом 
    def __init__(self, logger:MedaLogging):
        self.logger = logger

        
        self.HOST = '192.168.88.5'
        self.PORT = 2281
        
        self.telemetria = True
        self.checkConnect = True      
        # Настройки клиента 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
        self.client.connect((self.HOST, self.PORT))  # подключение адресс  порт

    def ClientDispatch(self, data:dict):
        #Функция для  отправки пакетов на пульт 
        if self.checkConnect:
            data['time'] = str(datetime.now())
            self.logger.debug(str(data))
            DataOutput = str(data).encode("utf-8")
            self.client.send(DataOutput)

    def ClientReceivin(self):
        #Прием информации с поста управления 
        if self.checkConnect:
            data = self.client.recv(512).decode('utf-8')
            if len(data) == 0:
                self.checkConnect = False
                self.logger.info('Rov-disconect')
                self.client.close()
                return None
            data = dict(literal_eval(str(data)))
            self.logger.debug(str(data))
            return data