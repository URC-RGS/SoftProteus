from configparser import ConfigParser  # чтание конфигов
from distutils import util
from RovCommunication import RovClient
from RovLogging import RovLogger
from RovHardwere import *



PATH_CONFIG = 'C:/Users/Yarik/Documents/SoftProteus-main/0.1/simulator-raspberry/'
PATH_LOG = PATH_CONFIG + 'log/'


class MainApparat:
    def __init__(self):
        # считываем конфиг
        self.config = ConfigParser()
        self.config.read(PATH_CONFIG + 'config_rov_debag.ini')

        # конфиг для логера 
        self.log_config = {'path_log': PATH_LOG,
                           'log_level': str(self.config['Rov']['log_level'])}
                           
        self.logi = RovLogger(self.log_config)
        
        self.client_config = {'logger': self.logi,
                              'local_host': str(self.config['Rov']['local_host']),
                              'port_local_host': int(self.config['Rov']['port_local_host']),
                              'real_host': str(self.config['Rov']['real_host']),
                              'port_real_host': int(self.config['Rov']['port_real_host']),
                              'local_host_start':util.strtobool(self.config['Rov']['local_host_start'])}

        self.client = RovClient(self.client_config)

        self.sensor = ReqiestSensor_debag(self.logi)

        self.comandor = Command_debag(self.logi)


    def RunMainApparat(self):
        # прием информации с поста управления
        # отработка по принятой информации
        # сбор информации с датчиков
        # отправка телеметрии на пост управления
        while True:
            data = self.client.receiver_data()
            if data != None:
                self.controllmass = data  # прием информации с поста управления
            else:
                continue

            self.comandor.commanda(self.controllmass)
            # сбор информации с датчиков и отправка на пост управления
            dataout = self.sensor.reqiest()
            dataout['time'] = data['time']
            self.client.send_data(dataout)



if __name__ == '__main__':
    apparat = MainApparat()
    apparat.RunMainApparat()
