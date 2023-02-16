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


class ServerMainPult:
    '''
    Класс описывающий систему бекенд- пульта
    log - флаг логирования 
    log cmd - флаг вывода логов с cmd 
    host - хост на котором будет крутиться сервер 
    port- порт для подключения 
    motorpowervalue=1 - программное ограничение мощности моторов 
    joystickrate - частота опроса джойстика 
    '''

    def __init__(self, logger: MedaLogging, debug=False):
        # инициализация атрибутов
        self.telemetria = False
        self.checkConnect = False
        self.logger = logger
        # выбор режима: Отладка\Запуск на реальном аппарате
        if debug:
            self.HOST = '127.0.0.1'
            self.PORT = 1136
        else:
            self.HOST = '192.168.88.5'
            self.PORT = 2281

        # настройка сервера
        self.server = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind((self.HOST, self.PORT))
        self.logger.info('ROV - waiting for connection')
        self.checkConnect = True
        self.bufferSize = 1024
        self.clientAdress = ''

        self.logger.info(f'ROV - Connected - {self.user_socket}')

    def ReceiverProteus(self):
        '''Прием информации с аппарата'''
        if self.checkConnect:
            data, self.clientAdress = self.server.recvfrom(self.bufferSize)
            if len(data) == 0:
                self.server.close()
                self.checkConnect = False
                self.logger.info(f'ROV - disconnection - {self.user_socket}')
                return None
            data = dict(literal_eval(str(data.decode('utf-8'))))
            if self.telemetria:
                self.logger.debug(f'DataInput - {str(data)}')
            return data

    def ControlProteus(self, data: dict):
        '''Отправка массива на аппарат'''
        if self.checkConnect:
            self.server.sendto(str(data).encode('utf-8'), self.clientAdress)
            if self.telemetria:
                self.logger.debug(str(data))


if __name__ == '__main__':
    ser = ServerMainPult(MedaLogging)
    while True:
        print(ser.ReceiverProteus())
        ser.ControlProteus({1:1,2:1,3:1})

