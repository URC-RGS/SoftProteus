import sys
from datetime import datetime
from distutils import util
from configparser import ConfigParser
from PyQt5 import QtCore
from RovCommunication import RovServer
from RovLogging import RovLogger
from RovControl import RovController
import threading
from design import *


# запуск на ноутбуке 
PATH_CONFIG = '/home/yarik/Документы/SoftProteus/UpperPC-GUI/'
PATH_LOG = PATH_CONFIG + '.log/'


class RovPultServer(QtCore.QObject):
    '''Класс отвечающий за общение с роботом и джойстиком'''
    rov_telemetry = QtCore.pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        
        # считываем конфиг
        self.config = ConfigParser()
        self.config.read(PATH_CONFIG + 'config_pult.ini')

        # конфиг для пульта управления 
        self.rov_conf = dict(self.config['RovPult'])

        # конфиг для логера 
        self.log_config = {'path_log': PATH_LOG,
                           'log_level': str(self.config['RovPult']['log_level'])}

        # создаем экземпляр отвечающий за логирование 
        self.logi = RovLogger(self.log_config)

        self.server_config = {'logger': self.logi,
                              'host': str(self.rov_conf['host']),
                              'port': int(self.rov_conf['port'])
                              }

        # обьект сервера 
        self.server = RovServer()

        # конфиг для джойстика 
        self.joi_config = dict(self.config['JOYSTICK'])
        self.joi_config['logger'] = self.logi

        # создаем экземпляр отвечающий за управление и взаимодействие с джойстиком 
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
        self.data_input = {}

        # частота оптправки
        self.rate_command_out = int(self.rov_conf['rate_command_out'])

        # флаг убийства сервера
        self.check_kill = False

        self.mass_rate = []

        self.logi.info('Main post init')

    def run_command(self):
        '''Основной цикл взаимодействия с аппаратом'''
        self.server.listen_to_connection(self.server_config)

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

            j1_val_y = transformation(data['ly'])
            j1_val_x = transformation(data['lx'])
            j2_val_y = transformation(data['ry'])
            j2_val_x = transformation(data['rx'])

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
            self.rov_telemetry.emit(self.data_input)

            # Проверка условия убийства сокета
            if self.check_kill:
                self.server.server.close()
                self.logi.info('command stop')
                break

            QtCore.QThread.msleep(self.rate_command_out)  

       
class ApplicationGUI(QMainWindow, Ui_UpperPCGUI):
    '''Основной класс приложения'''
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # создание потоков для опроса джойстика и связи с роботом 
        self.thread_server = QtCore.QThread()
        self.thread_joi = QtCore.QThread()

        # создание обьекта сервера для взаимодействия с роботом и опроса джойстика 
        self.server = RovPultServer()

        # подключение действий к кнопкам 
        self.button_connect.clicked.connect(self.connect)
        self.button_apply.clicked.connect(self.apply)

        # считывание конфига и вывод на гафику значений из конфиг файла по умолчанию 
        self.host_value.setText(self.server.server_config['host'])
        self.port_value.setText(str(self.server.server_config['port']))

        self.f_b_set.setCurrentText(self.server.joi_config['move_forward_back'])
        self.l_r_set.setCurrentText(self.server.joi_config['move_left_right'])
        self.u_d_set.setCurrentText(self.server.joi_config['move_up_down'])
        self.tl_tr_set.setCurrentText(self.server.joi_config['move_turn_left_turn_righ'])

        self.f_b_value.setValue(float(self.server.joi_config['forward_back_power']))
        self.l_r_value.setValue(float(self.server.joi_config['left_right_power']))
        self.u_d_value.setValue(float(self.server.joi_config['up_down_power']))
        self.tl_tr_value.setValue(float(self.server.joi_config['turn_left_turn_righ_power']))

        self.camera_up_set.setCurrentText(self.server.joi_config['camera_up'])
        self.camera_dowm_set.setCurrentText(self.server.joi_config['camera_down'])

        self.arm_up_set.setCurrentText(self.server.joi_config['arm_up'])
        self.arm_down_set.setCurrentText(self.server.joi_config['arm_down'])

        self.led_on_set.setCurrentText(self.server.joi_config['led_on'])
        self.led_off_set.setCurrentText(self.server.joi_config['led_off'])

    
    def connect(self):
        '''Запуск сервера для подключения аппарата'''

        # получение адреса и порта для создание сокета 
        self.server.server_config['host'] = self.host_value.text()
        self.server.server_config['port'] = int(self.port_value.text())
        
        # создание сокета и вынос его в отдельный поток 
        self.server.moveToThread(self.thread_server)
        self.server.rov_telemetry.connect(self.updategui)
        self.thread_server.started.connect(self.server.run_command)
        self.thread_server.start()

        # запуск потока для опроса джойстика 
        self.start_joi()

        # деактивация кнопок и полей для ввода адреса и порта 
        self.button_connect.setEnabled(False)
        self.host_value.setEnabled(False)
        self.port_value.setEnabled(False)
    
    def start_joi(self):
        '''Запуск потока для опроса джойстика'''
        self.server.controll_ps4.moveToThread(self.thread_joi)
        self.thread_joi.started.connect(self.server.controll_ps4.listen)
        self.thread_joi.start()

    def apply(self):
        '''Обработка настроек управления из GUI '''
        self.server.controll_ps4.forward_back = self.f_b_value.value() * 32767
        self.server.controll_ps4.left_right = self.l_r_value.value() * 32767
        self.server.controll_ps4.up_down = self.u_d_value.value() * 32767
        self.server.controll_ps4.turn_left_turn_righ = self.tl_tr_value.value() * 32767

        self.server.controll_ps4.move_forward_back = int(self.server.joi_config[str(self.f_b_set.currentText().encode('latin-1'))[2:-1]])
        self.server.controll_ps4.move_left_right = int(self.server.joi_config[str(self.l_r_set.currentText().encode('latin-1'))[2:-1]])
        self.server.controll_ps4.move_up_down = int(self.server.joi_config[str(self.u_d_set.currentText().encode('latin-1'))[2:-1]])
        self.server.controll_ps4.move_turn_left_turn_righ = int(self.server.joi_config[str(self.tl_tr_set.currentText().encode('latin-1'))[2:-1]])

    def updategui(self, telemetry):
        # вывод телеметрии в графику 
        self.term_value.display(telemetry['term'])
        self.depth_value.display(telemetry['depth'])
        self.orientation_value.display(telemetry['orientation'])

        self.angle_x_value.display(0)
        self.angle_y_value.display(0)
        self.angle_z_value.display(0)

        self.amperage_value.display(telemetry['amp'])
        self.voltage_value.display(telemetry['volt'])
        self.charge_value.display(100)


if __name__ == '__main__':
    # если файл запущен как основной то запуск приложения
    app = QApplication(sys.argv)
    ex = ApplicationGUI()
    ex.show()
    sys.exit(app.exec_())
