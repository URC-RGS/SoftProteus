import board
import busio
from time import sleep  # библиотека длязадержек
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_servokit import ServoKit
import FaBo9Axis_MPU9250
from math import atan2, pi
import ms5837
from RovLogging import RovLogger

class Acp:
    def __init__(self, logger: RovLogger):
        '''
        Класс описывающий взаимодействие и опрос датчиков тока
        '''
        self.logger = logger
        try:
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.ads13 = ADS.ADS1115(self.i2c)
            self.adc46 = ADS.ADS1115(self.i2c, address=0x49)
            a0 = AnalogIn(self.ads13, ADS.P0)
            a1 = AnalogIn(self.ads13, ADS.P1)
            a2 = AnalogIn(self.ads13, ADS.P2)
            a3 = AnalogIn(self.adc46, ADS.P3)
            a4 = AnalogIn(self.adc46, ADS.P0)
            a5 = AnalogIn(self.adc46, ADS.P1)
            

            self.CorNulA1 = a0.value
            self.CorNulA2 = a1.value
            self.CorNulA3 = a2.value
            self.CorNulA4 = a3.value
            self.CorNulA5 = a4.value
            self.CorNulA6 = a5.value
            self.logger.info('ADC1115-init')
        except:
            self.logger.critical('NO-ADC1115')
        
        self.MassOut = {}

    def ReqestAmper(self):
        try:
            #Функция опроса датчиков тока 
            a0 = AnalogIn(self.ads13, ADS.P0)
            a1 = AnalogIn(self.ads13, ADS.P1)
            a2 = AnalogIn(self.ads13, ADS.P2)
            a3 = AnalogIn(self.ads13, ADS.P3)
            a4 = AnalogIn(self.adc46, ADS.P0)
            a5 = AnalogIn(self.adc46, ADS.P1)
            v = AnalogIn(self.adc46, ADS.P2)
            # TODO  матан для перевода значений - отсылается уже в амперах
            self.MassOut['a0'] = round(
                (a0.value - self.CorNulA1) * 0.00057321919, 3)
            self.MassOut['a1'] = round(
                (a1.value - self.CorNulA2) * 0.00057321919, 3)
            self.MassOut['a2'] = round(
                (a2.value - self.CorNulA3) * 0.00057321919, 3)
            self.MassOut['a3'] = round(
                (a3.value - self.CorNulA4) * 0.00057321919, 3)
            self.MassOut['a4'] = round(
                (a4.value - self.CorNulA5) * 0.00057321919, 3)
            self.MassOut['a5'] = round(
                (a5.value - self.CorNulA6) * 0.00057321919, 3)
            
            self.MassOut['v'] = round(v.voltage * 5, 3)
            # возвращает словарь с значениями амрепметра нумерация с нуля
            return self.MassOut
        except:
            self.logger.critical('NO-ADC1115')
            return None


class Compass:
    # класс описывающий общение с модулем навигации mpu9250
    def __init__(self, logger: RovLogger):
        self.logger = logger
        
        try:
            self.mpu9250 = FaBo9Axis_MPU9250.MPU9250()
            self.logger.info('MPU9250-init')
        except:
            self.logger.critical('NO-MPU9250')
    
    def reqiest(self):
        # возвращает словарь с значениями азимута
        try:
            mag = self.mpu9250.readMagnet()
            return {'azim':(round((atan2(mag['x'], mag['y']) * 180 / pi), 3))}
        except:
            self.logger.critical('NO-MPU9250')
            return None


class DeptAndTemp:
    # класс описывающий общение с датчиком глубины 
    def __init__(self, logger: RovLogger):
        
        self.logger = logger
        # плотность воды 
        density = 1000 
        # илициализация сенсора 
        self.sensor  = ms5837.MS5837_30BA()
        if self.sensor.init():
            self.sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
            self.sensor.setFluidDensity(density)
            self.dept_defolt = round(self.sensor.depth(), 3)
            self.logger.info('DEPT-SENSOR-init')
        else:
            self.logger.critical('NO-SENSOR-DEPT')


    def reqiest(self):
        # опрос датчика давления
        if self.sensor.read():
            massout = {}
            massout['dept'] = round(self.sensor.depth(), 3) - self.dept_defolt - 10.4
            #print('dept: ', massout['dept'])
            massout['term'] = round(self.sensor.temperature(), 3)
            return massout
        else:
            self.logger.critical('NO-SENSOR-DEPT')
            return {'dept':-100,'temp': -100}


class PwmControl:
    def __init__(self, config:dict):
        self.logger = config['logi']
        # диапазон шим модуляции 
        self.pwmMin = 1100
        self.pwmMax = 1950
        # коофиценты корректировки мощности на каждый мотор 
        self.CorDrk0 = 1
        self.CorDrk1 = 1
        self.CorDrk2 = 1
        self.CorDrk3 = 1
        self.CorDrk4 = 1
        self.CorDrk5 = 1
        # инициализация платы 
        try:
            self.kit = ServoKit(channels=16)
            self.logger.info('PWM-CONTROL-init')
        except:
            self.logger.critical('NO-PWM-CONTROL')

        self.drk0 = self.kit.servo[config['pin_motor_0']]
        self.drk0.set_pulse_width_range(self.pwmMin, self.pwmMax)
        self.drk1 = self.kit.servo[config['pin_motor_1']]
        self.drk1.set_pulse_width_range(self.pwmMin, self.pwmMax)
        self.drk2 = self.kit.servo[config['pin_motor_2']]
        self.drk2.set_pulse_width_range(self.pwmMin, self.pwmMax)
        self.drk3 = self.kit.servo[config['pin_motor_3']]
        self.drk3.set_pulse_width_range(self.pwmMin, self.pwmMax)
        self.drk4 = self.kit.servo[config['pin_motor_4']]
        self.drk4.set_pulse_width_range(self.pwmMin, self.pwmMax)
        self.drk5 = self.kit.servo[config['pin_motor_5']]
        self.drk5.set_pulse_width_range(self.pwmMin, self.pwmMax)
        
        # взаимодействие с манипулятором 
        self.man = self.kit.servo[config['pin_man']]
        self.man.set_pulse_width_range(self.pwmMin, self.pwmMax)
        self.man.angle = 0
        
        # взаимодействие с сервоприводом камеры 
        self.servoCam = self.kit.servo[config['pin_servo_cam']]
        
        self.servoCam.angle = 90
        
        # взаимодействие с светильником 
        self.led = self.kit.servo[config['pin_led']]
        
        self.led.angle = 0
        
        # инициализация моторов 
        self.drk0.angle = 180
        self.drk1.angle = 180
        self.drk2.angle = 180
        self.drk3.angle = 180
        self.drk4.angle = 180
        self.drk5.angle = 180
        sleep(2)
        self.drk0.angle = 0
        self.drk1.angle = 0
        self.drk2.angle = 0
        self.drk3.angle = 0
        self.drk4.angle = 0
        self.drk5.angle = 0
        sleep(2)
        self.drk0.angle = 87
        self.drk1.angle = 87
        self.drk2.angle = 87
        self.drk3.angle = 87
        self.drk4.angle = 87
        self.drk5.angle = 87
        sleep(3)

    def ControlMotor(self, mass: dict):
        # отправка шим сигналов на моторы
        self.drk0.angle = mass['motor_0']
        self.drk1.angle = mass['motor_1']
        self.drk2.angle = mass['motor_2']
        self.drk3.angle = mass['motor_3']
        self.drk4.angle = mass['motor_4']
        self.drk5.angle = mass['motor_5']
        
        self.man.angle = mass['man']
        
        self.servoCam.angle = mass['servo_сam']
        
        if mass['led']:
            self.led.angle = 180 
        else:
            self.led.angle = 0


class ReqiestSensor:
    # класс-адаптер обьеденяющий в себе сбор информации с всех сенсоров 
    def __init__(self, logger):
        self.logger = logger
        self.acp = Acp(self.logger) # обект класса ацп 
        self.mpu9250 = Compass(self.logger) # обьект класса compass 
        self.ms5837 = DeptAndTemp(self.logger)
    
    def reqiest(self):
        # опрос датчиков; возвращает обьект класса словарь 
        massacp  = self.acp.ReqestAmper()
        massaz = self.mpu9250.reqiest()
        #print('azim: ', massaz['azim'])
        massMs5837 = self.ms5837.reqiest()
        
        massout = {**massacp, **massaz, **massMs5837}
        
        return massout
   
   
class Command:
    def __init__(self, config):
        self.config = config
        self.logger = config['logi']
        self.pwmcom = PwmControl(self.config)
    
    def safety(self, value):
        if value < 0:
            return 0
        elif value > 180:
            return 180
        else:
            return value
        
    def commanda(self, command):
        if self.config['reverse_motor_0']:
            command['motor_0'] = self.safety((180 - command['motor_0'] * 1.8) - 3)
        else: 
            command['motor_0'] = self.safety((command['motor_0'] * 1.8) - 3)
            
        if self.config['reverse_motor_1']:
            command['motor_1'] = self.safety((180 - command['motor_1'] * 1.8) - 3)
        else:
            command['motor_1'] = self.safety((command['motor_1'] * 1.8) - 3)
        
        if self.config['reverse_motor_2']:
            command['motor_2'] = self.safety((180 - command['motor_2'] * 1.8) - 3)
        else:
            command['motor_2'] = self.safety((command['motor_2'] * 1.8) - 3)
            
        if self.config['reverse_motor_3']:
            command['motor_3'] = self.safety((180 - command['motor_3'] * 1.8) - 3)
        else:
            command['motor_3'] = self.safety((command['motor_3'] * 1.8) - 3)
            
        if self.config['reverse_motor_4']:
            command['motor_4'] = self.safety((180 - command['motor_4'] * 1.8) - 3)
        else:
            command['motor_4'] = self.safety((command['motor_4'] * 1.8) - 3)
            
        if self.config['reverse_motor_5']:
            command['motor_5'] = self.safety((180 - command['motor_5'] * 1.8) - 3)
        else:
            command['motor_5'] = self.safety((command['motor_5'] * 1.8) - 3)
            
        self.pwmcom.ControlMotor(command)
