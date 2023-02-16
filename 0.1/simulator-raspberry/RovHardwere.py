from time import sleep  
from datetime import datetime  
from RovLogging import RovLogger
from random import randint, random, uniform
from time import sleep  
from math import atan2, pi


class Acp_debag:
    def __init__(self, logger: RovLogger):
        '''
        Класс описывающий взаимодействие и опрос датчиков тока
        '''
        self.logger = logger
        self.logger.info('ADC1115-init')

        self.MassOut = {}

    def ReqestAmper(self):
        return {'a0':round(random(),2), 'a1':round(random(),2), 'a2':round(random(),2),'a2':round(random(),2),
                'a3':round(random(),2), 'a4':round(random(),2), 'a5':round(random(),2)}


class Compass_debag:
    # класс описывающий общение с модулем навигации mpu9250
    def __init__(self, logger: RovLogger):
        self.logger = logger
        self.logger.info('MPU9250-init')
   
    def reqiest(self):
        # возвращает словарь с значениями азимута
        return {'azim': randint(180,210)}


class DeptAndTemp_debag:
    # класс описывающий общение с датчиком глубины
    def __init__(self, logger: RovLogger):

        self.logger = logger
        # илициализация сенсора
        self.logger.info('DEPT-SENSOR-init')

    def reqiest(self):
        # опрос датчика давления
        massout = {}
        massout['dept'] = round(uniform(0,2),2)
        massout['term'] = round(uniform(20,25),2)
        return massout


class PwmControl_debag:
    def __init__(self, logger: RovLogger):
        self.logger = logger
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
        #  
        self.logger.info('PWM-CONTROL-init')

    def ControlMotor(self, mass: dict):
        # отправка шим сигналов на моторы
        pass


class ReqiestSensor_debag:
    # класс-адаптер обьеденяющий в себе сбор информации с всех сенсоров
    def __init__(self, logger: RovLogger):
        self.logger = logger
        self.acp = Acp_debag(self.logger)  # обект класса ацп
        self.mpu9250 = Compass_debag(self.logger)  # обьект класса compass
        self.ms5837 = DeptAndTemp_debag(self.logger)

    def reqiest(self):
        # опрос датчиков; возвращает обьект класса словарь
        massacp = self.acp.ReqestAmper()
        massaz = self.mpu9250.reqiest()
        massMs5837 = self.ms5837.reqiest()

        massout = {**massacp, **massaz, **massMs5837}

        return massout


class Command_debag:
    def __init__(self, logger):
        self.logger = logger
        self.pwmcom = PwmControl_debag(self.logger)

    def safety(self, value):
        if value < 0:
            return 0
        elif value > 180:
            return 180
        else:
            return value

    def commanda(self, command):
        command['motor_0'] = self.safety((180 - command['motor_0'] * 1.8) - 3)
        command['motor_1'] = self.safety((command['motor_1'] * 1.8) - 3)
        command['motor_2'] = self.safety((command['motor_2'] * 1.8) - 3)
        command['motor_3'] = self.safety((180 - command['motor_3'] * 1.8) - 3)
        command['motor_4'] = self.safety((180 - command['motor_4'] * 1.8) - 3)
        command['motor_5'] = self.safety((180 - command['motor_5'] * 1.8) - 3)
        self.pwmcom.ControlMotor(command)
