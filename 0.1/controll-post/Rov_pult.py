import threading
from datetime import datetime
from distutils import util
from configparser import ConfigParser
from PyQt5 import QtCore
from RovCommunication import RovServer
from RovLogging import RovLogger
from RovControl import RovController

# запуск на ноутбуке 
PATH_CONFIG = 'C:/Users/Yarik/Documents/SoftProteus-main/0.1/controll-post/'
PATH_LOG = 'C:/Users/Yarik/Documents/SoftProteus-main/0.1/controll-post/log/'


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
        self.data_output = {'time': datetime.now(),  # Текущее время
                           'motor_power_value': 1,  # мощность моторов
                           'led': False,  # управление светом
                           'man': 0,  # Управление манипулятором
                           'servo_сam': 90,  # управление наклоном камеры
                           'motor_0': 0, 'motor_1': 0,  # значения мощности на каждый мотор
                           'motor_2': 0, 'motor_3': 0,
                           'motor_4': 0, 'motor_5': 0}

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
        '''
        Движение вперед - (1 вперед 2 вперед 3 назад 4 назад) 
        Движение назад - (1 назад 2 назад 3 вперед 4 вперед)
        Движение лагом вправо - (1 назад 2 вперед 3 вперед 4 назад)
        Движение лагом влево - (1 вперед 2 назад 3 назад 4 вперед)
        Движение вверх - (5 вниз 6 вниз)
        Движение вниз - (5 вверх 6 вверх)
        '''
        def transformation(value: int):
            # Функция перевода значений АЦП с джойстика в проценты
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
            # счетчик частоты 
            deley = datetime.now() - self.data_input['time']
            deley = deley.total_seconds()
            self.mass_rate.append(round(1 / deley))
            if len(self.mass_rate) >= 100:
                print(sum(self.mass_rate) // 100)
                self.mass_rate = []

            # запрос данный из класса пульта (потенциально слабое место)
            data = self.data_pult

            # математика преобразования значений с джойстика в значения для моторов
            
            self.logi.debug(f'Data pult: {data}')

            j1_val_y = transformation(data['j1_val_y'])
            j1_val_x = transformation(data['j1_val_x'])
            j2_val_y = transformation(data['j2_val_y'])
            j2_val_x = transformation(data['j2_val_x'])

            # Подготовка массива для отправки на аппарат
            self.data_output['motor_0'] = defense(j1_val_x + j1_val_y - j2_val_x)
            self.data_output['motor_1'] = defense(j1_val_x - j1_val_y - j2_val_x + 100)
            self.data_output['motor_2'] = defense((-1 * j1_val_x) - j1_val_y - j2_val_x + 200)
            self.data_output['motor_3'] = defense((-1 * j1_val_x) + j1_val_y - j2_val_x + 100)

            self.data_output['motor_4'] = defense(j2_val_y)
            self.data_output['motor_5'] = defense(j2_val_y)

            self.data_output["time"] = str(datetime.now())

            self.data_output['led'] = data['led']

            # данные для манипулятора
            if data['man']:
                self.data_output['man'] = 180
            else:
                self.data_output['man'] = 0

            # данные для сервы камеры
            self.data_output['servo_сam'] = abs(data['servo_сam'])

            # отправка и прием сообщений
            self.server.send_data(self.data_output)

            self.data_input = self.server.receiver_data()
            self.data_input['time'] = datetime.strptime(self.data_input['time'], '%Y-%m-%d %H:%M:%S.%f')

            # TODO сделать вывод телеметрии на инжинерный экран 
            #print(self.data_input)

            # Проверка условия убийства сокета
            if self.check_kill:
                self.server.server.close()
                self.logi.info('command stop')
                break

            QtCore.QThread.msleep(self.rate_command_out)
            #sleep(self.rate_command_out)

    def run_main(self):
        '''запуск процессов опроса джойстика и основного цикла программы'''
        self.thread_joi = threading.Thread(target=self.run_controller)
        self.thread_com = threading.Thread(target=self.run_command)

        self.thread_joi.start()
        self.thread_com.start()


if __name__ == '__main__':
    post = RovPost()
    post.run_main()