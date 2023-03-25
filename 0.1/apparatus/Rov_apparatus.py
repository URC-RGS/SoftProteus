from configparser import ConfigParser
from distutils import util
from RovHardwere import ReqiestSensor, Command
from RovCommunication import RovClient
from RovLogging import RovLogger
import subprocess

# user: Prot password: rov

# запуск на одноплатном компьютере Raspberry pi4 
PATH_CONFIG = '/home/Prot/SoftProteus/0.1/apparatus/' 
PATH_LOG = '/home/Prot/SoftProteus/0.1/apparatus/log/'


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
        
        self.sensor = ReqiestSensor(self.logi)
        
        self.comandor_config = {'logi': self.logi,
                                'reverse_motor_0':util.strtobool(self.config['Rov']['reverse_motor_0']),
                                'reverse_motor_1':util.strtobool(self.config['Rov']['reverse_motor_1']),
                                'reverse_motor_2':util.strtobool(self.config['Rov']['reverse_motor_2']),
                                'reverse_motor_3':util.strtobool(self.config['Rov']['reverse_motor_3']),
                                'reverse_motor_4':util.strtobool(self.config['Rov']['reverse_motor_4']),
                                'reverse_motor_5':util.strtobool(self.config['Rov']['reverse_motor_5']),
                                
                                'pin_motor_0':int(self.config['Rov']['pin_motor_0']),
                                'pin_motor_1':int(self.config['Rov']['pin_motor_1']),
                                'pin_motor_2':int(self.config['Rov']['pin_motor_2']),
                                'pin_motor_3':int(self.config['Rov']['pin_motor_3']),
                                'pin_motor_4':int(self.config['Rov']['pin_motor_4']),
                                'pin_motor_5':int(self.config['Rov']['pin_motor_5']),
                                
                                'pin_man':int(self.config['Rov']['pin_man']),
                                
                                'pin_servo_cam':int(self.config['Rov']['pin_servo_cam']),
                                
                                'pin_led':int(self.config['Rov']['pin_led'])}

        self.comandor = Command(self.comandor_config)
        
        #subprocess.run('libcamera-vid --width 1280 --height 720 -t 0 --inline -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=192.168.88.251 port=9000 &')
        self.logi.info('start gstremmer')

        
    def RunMainApparat(self):
        try:
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
        except:
            pass


if __name__ == '__main__':
    apparat = MainApparat()
    apparat.RunMainApparat()

