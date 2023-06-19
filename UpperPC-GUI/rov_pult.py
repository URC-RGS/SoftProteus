import sys
from datetime import datetime
from distutils import util
from configparser import ConfigParser
from PyQt5 import QtCore
from RovCommunication import RovServer
from RovLogging import RovLogger
from RovControl import RovController
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import *



# запуск на ноутбуке 
PATH_CONFIG = '/home/yarik/Документы/SoftProteus/UpperPC-GUI/'
PATH_LOG = PATH_CONFIG + '.log/'


class RovPultServer(QtCore.QObject):

    commandserver = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()

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

        self.server.listen_to_connection()

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


class ApplicationGUI(QMainWindow, Ui_UpperPCGUI):
    def __init__(self):
        # импорт и создание интерфейса
        super().__init__()
        self.setupUi(self)

        self.button_connect.clicked.connect(self.connect)
        self.button_disconnect.clicked.connect(self.disconnect)
        self.button_apply.clicked.connect(self.apply)
        self.updategui({})

        # создание потоков и привязка
        self.thread = QtCore.QThread()
        
    def read(self):
        # TODO доделать подтягивание из конфиг файла 
        pass

    def connect(self):
        host = self.host_value.text()
        port = self.port_value.text()
        print(host, port)
        self.start_server()

    def disconnect(self):
        self.threadserver.server.server.close()
        self.thread.terminate()

        
    def apply(self):
        #f_b_set = self.f_b_set.value()
        f_b_value = self.f_b_value.value()
        #l_r_set = self.l_r_set.value()
        l_r_value = self.l_r_value.value()
        #u_d_set = self.u_d_set.value()
        u_d_value = self.u_d_value.value()
        #tl_tr_set = self.tl_tr_set.value()
        tl_tr_value = self.tl_tr_value.value()

        #camera_up_set = self.camera_up_set.value()
        #camera_down_set = self.camera_dowm_set.value()

        #arm_up_set = self.arm_up_set.value()
        #arm_down_set = self.arm_down_set.value()

        #led_on_set = self.led_on_set.value()
        #led_off_set = self.led_off_set.value()

        print(f_b_value, l_r_value, u_d_value, tl_tr_value)


    def start_server(self):
        # запуск сервера
        self.threadserver = RovPultServer()
        self.threadserver.moveToThread(self.thread)
        self.threadserver.commandserver.connect(self.updategui)
        self.thread.started.connect(self.threadserver.run_command)
        self.thread.start()
        print(12233)

    def start_joi(self):
        # self.threadJoi = threading.Thread(target=self.threadserver.run_controller)
        # self.threadJoi.start()
        pass

    @QtCore.pyqtSlot()
    def updategui(self, dataMass):

        self.term_value.display(1)
        self.depth_value.display(2)
        self.orientation_value.display(3)

        self.angle_x_value.display(4)
        self.angle_y_value.display(5)
        self.angle_z_value.display(6)

        self.amperage_value.display(7)
        self.voltage_value.display(8)
        self.charge_value.display(9)


class RovPost:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ex = ApplicationGUI()

    def ShowApplication(self):
        self.ex.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    application = RovPost()
    application.ShowApplication()