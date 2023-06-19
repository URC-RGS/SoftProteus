from configparser import ConfigParser
from distutils import util
from RovCommunication import RovClient, Rov_SerialPort
from RovLogging import RovLogger
from datetime import datetime


# запуск на одноплатном компьютере Raspberry pi4 
PATH_CONFIG = '/home/yarik/Документы/SoftProteus/MedianRaspberry/' 
PATH_LOG = PATH_CONFIG + '.log/'


class MainApparat:
    def __init__(self):
        # считываем конфиг
        self.config = ConfigParser()
        self.config.read(PATH_CONFIG + 'config_rov.ini')
        
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
        
        self.serial_port_config = {
                                    'logger': self.logi,
                                    'port': str(self.config['Rov']['port']),
                                    'bitrate': int(self.config['Rov']['bitrate']),
                                    'timeout': float(self.config['Rov']['timeout'])
                                    }
        self.serial_port = Rov_SerialPort(self.serial_port_config)
        
        self.telemetry = {'date': str(datetime.now())}
        
        
    def update_telemetry(self):
        self.telemetry = {'date': str(datetime.now())}


    def RunMainApparat(self):
        try:
            while True:
                data_in = self.client.receiver_data()
                self.logi.debug(data_in)
                if data_in != None:
                    self.controllmass = data_in  # прием информации с поста управления
                else:
                    continue
            
                lower_out = [
                    self.controllmass['m_0'],
                    self.controllmass['m_1'],
                    self.controllmass['m_2'],
                    self.controllmass['m_3'],
                    self.controllmass['m_4'],
                    self.controllmass['m_5'],
                    self.controllmass['m_6'],
                    self.controllmass['m_7']
                    ]
                
                self.serial_port.send_data_new(lower_out)
                
                self.telemetry_lower = self.serial_port.receiver_data_new()

                self.update_telemetry()
                
                self.logi.debug(self.telemetry)
                self.client.send_data(self.telemetry)
        except:
            pass


if __name__ == '__main__':
    apparat = MainApparat()
    apparat.RunMainApparat()

