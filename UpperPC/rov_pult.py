import os
import pyautogui
import numpy as np
import threading
from datetime import datetime
from distutils import util
from configparser import ConfigParser
from PyQt5 import QtCore
from RovCommunication import RovServer
from RovLogging import RovLogger
from RovControl import RovController


# запуск на ноутбуке 
PATH_CONFIG = '/home/yarik/Документы/SoftProteus/UpperPC/'
PATH_LOG = PATH_CONFIG + '.log/'


class RovPost:
    def __init__(self):
        # считываем конфиг
        self.config = ConfigParser()
        self.config.read(PATH_CONFIG + 'config_pult.ini')

        self.rov_conf = dict(self.config['RovPult'])

        # конфиг для логера 
        self.log_config = {'path_log': PATH_LOG,
                           'log_level': str(self.config['RovPult']['log_level'])}

        # создаем экземпляр класса отвечающий за логирование 
        self.logi = RovLogger(self.log_config)

        self.server_config = {'logger': self.logi,
                              'local_host': str(self.rov_conf['local_host']),
                              'port_local_host': int(self.rov_conf['port_local_host']),
                              'real_host': str(self.rov_conf['real_host']),
                              'port_real_host': int(self.rov_conf['port_real_host']),
                              'local_host_start':util.strtobool(self.rov_conf['local_host_start'])}

        # поднимаем связь с аппаратом
        self.server = RovServer(self.server_config)

        # конфиг для джойстика 
        self.joi_config = dict(self.config['JOYSTICK'])
        self.joi_config['logger'] = self.logi

        # создаем экземпляр класса отвечающий за управление и взаимодействие с джойстиком 
        self.controll_ps4 = RovController(self.joi_config)  

        # подтягиваем данные с джойстика 
        self.data_pult = self.controll_ps4.data_pult

        # словарик для отправки на аппарат
        self.data_output = {'led': False,  # управление светом
                           'man': 0,  # управление манипулятором
                           'servo_сam': 90,  # управление наклоном камеры
                           'm_0': 50,
                           'm_1': 50,
                           'm_2': 50,
                           'm_3': 50,
                           'm_4': 50,
                           'm_5': 50,
                           'm_6': 50,
                           'm_7': 50
                           }

        # словарик получаемый с аппарата
        self.data_input = {'time': datetime.now(), 'dept': None,
                          'volt': None, 'azimut': None}

        # частота оптправки
        self.rate_command_out = int(self.rov_conf['rate_command_out'])

        self.check_kill = False

        self.mass_rate = []

        self.logi.info('Main post init')

    def run_controller(self):
        #запуск на прослушивание контроллера ps4
        self.controll_ps4.listen()

    def run_command(self):
        self.logi.info('Pult run')

        def transformation(value: int):
            # Функция перевода значений АЦП 
            value = (32768 - value) // 655
            return value

        def defense(value: int):
            # Функция защитник от некорректных данных
            if value > 100:
                value = 100
            elif value < 0:
                value = 0
            return value

        while True:
            data = self.data_pult

            # математика преобразования значений с джойстика в значения для моторов
            
            self.logi.debug(f'Data pult: {data}')

            j1_val_y = transformation(data['j1_val_y'])
            j1_val_x = transformation(data['j1_val_x'])
            j2_val_y = transformation(data['j2_val_y'])
            j2_val_x = transformation(data['j2_val_x'])



            # Подготовка массива для отправки на аппарат
            self.data_output['m_0'] = defense(j1_val_y - (50 - j1_val_x) - (50 - j2_val_y) - (50 - j2_val_x))
            self.data_output['m_1'] = defense(j1_val_y + (50 - j1_val_x) - (50 - j2_val_y) + (50 - j2_val_x))
            self.data_output['m_2'] = defense(j1_val_y + (50 - j1_val_x) + (50 - j2_val_y) + (50 - j2_val_x))
            self.data_output['m_3'] = defense(j1_val_y - (50 - j1_val_x) + (50 - j2_val_y) - (50 - j2_val_x))
            self.data_output['m_4'] = defense(j1_val_y + (50 - j1_val_x) + (50 - j2_val_y) - (50 - j2_val_x))
            self.data_output['m_5'] = defense(j1_val_y - (50 - j1_val_x) + (50 - j2_val_y) + (50 - j2_val_x))
            self.data_output['m_6'] = defense(j1_val_y - (50 - j1_val_x) - (50 - j2_val_y) + (50 - j2_val_x))
            self.data_output['m_7'] = defense(j1_val_y + (50 - j1_val_x) - (50 - j2_val_y) - (50 - j2_val_x))

            # отправка и прием сообщенийcd
            
            
            self.logi.debug(self.data_output)
            self.server.send_data(self.data_output)

            self.data_input = self.server.receiver_data()

            # Проверка условия убийства сокета
            if self.check_kill:
                self.server.server.close()
                self.logi.info('command stop')
                break

            QtCore.QThread.msleep(self.rate_command_out)

    def run_main(self):
        '''запуск процессов опроса джойстика и основного цикла программы'''
        self.thread_joi = threading.Thread(target=self.run_controller)
        self.thread_com = threading.Thread(target=self.run_command)

        self.thread_joi.start()
        self.thread_com.start()


if __name__ == '__main__':
    post = RovPost()
    post.run_main()