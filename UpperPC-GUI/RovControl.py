import os
import pygame
from distutils import util
from PyQt5 import QtCore


class RovController(QtCore.QObject):
    '''Класс опроса джойстика'''
    def __init__(self, config):
        super().__init__()

        os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.pygame = pygame
        self.pygame.init()

        self.joi_config = config

        joysticks = []
        for i in range(self.pygame.joystick.get_count()):
            joysticks.append(self.pygame.joystick.Joystick(i))
        for self.joystick in joysticks:
            self.joystick.init()

        self.logi = config['logger']

        self.data_pult = {'ly': 0, 'lx': 0,
                         'ry': 0, 'rx': 0,
                         'man': 0, 'servo_сam': 90,
                         'led': 0}
        
        self.camera_up = int(self.joi_config[self.joi_config['camera_up']])

        self.camera_down = int(self.joi_config[self.joi_config['camera_down']])

        self.arm_up =  int(self.joi_config[self.joi_config['arm_up']])

        self.arm_down =  int(self.joi_config[self.joi_config['arm_down']])

        self.led_on = int(self.joi_config[self.joi_config['led_on']])

        self.led_off = int(self.joi_config[self.joi_config['led_off']])

        self.sleep_listen = int(self.joi_config['time_sleep_joi'])

        self.forward_back = float(self.joi_config['forward_back_power']) * 32767

        self.min_value = float(self.joi_config['min_value'])

        self.move_forward_back = int(self.joi_config[self.joi_config['move_forward_back']])

        self.left_right = float(self.joi_config['left_right_power']) * 32767

        self.move_left_right = int(self.joi_config[self.joi_config['move_left_right']])

        self.move_up_down = int(self.joi_config[self.joi_config['move_up_down']])

        self.up_down = float(self.joi_config['up_down_power']) * 32767

        self.move_turn_left_turn_righ = int(self.joi_config[self.joi_config['move_turn_left_turn_righ']])

        self.turn_left_turn_righ = float(self.joi_config['turn_left_turn_righ_power']) * 32767

        self.reverse_forward_back = bool(util.strtobool(self.joi_config['reverse_forward_back']))

        self.reverse_left_right = bool(util.strtobool(self.joi_config['reverse_left_right']))

        self.reverse_up_down = bool(util.strtobool(self.joi_config['reverse_up_down']))

        self.reverse_turn_left_turn_righ = bool(util.strtobool(self.joi_config['reverse_turn_left_turn_righ']))
        
        self.min_value_cam = float(self.joi_config['min_value_cam'])
        
        self.max_value_cam = float(self.joi_config['max_value_cam'])

        self.running = True

        self.logi.info('Controller PS4 init')

    def listen(self):
        self.logi.info('Controller PS4 listen')

        # сдвиг камеры 
        cor_servo_cam = 0

        while self.running:
            for event in self.pygame.event.get():
                # опрос нажания кнопок
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == self.camera_up:
                        cor_servo_cam = -3

                    if event.button == self.camera_down:
                        cor_servo_cam = 3

                    if event.button == self.arm_up:
                        self.data_pult['man'] = 180

                    if event.button == self.arm_down:
                        self.data_pult['man'] = 0

                    if event.button == self.led_on:
                        self.data_pult['led'] = 1

                    if event.button == self.led_off:
                         self.data_pult['led'] = 0
                    
                if event.type == pygame.JOYBUTTONUP:
                    if event.button == self.camera_up:
                        cor_servo_cam = 0

                    if event.button == self.camera_down:
                        cor_servo_cam = 0

                # опрос стиков
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == self.move_forward_back:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_forward_back:
                            self.data_pult['ly'] = int(round(event.value, 2) * self.forward_back * -1)
                                
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_forward_back:
                            self.data_pult['ly'] = int(round(event.value, 2) * self.forward_back)
                            
                        else:
                            self.data_pult['ly'] = 0

                    if event.axis == self.move_left_right:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_left_right:
                            self.data_pult['lx'] = int(round(event.value, 2) * self.left_right * -1)

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_left_right:
                            self.data_pult['lx'] = int(round(event.value, 2) * self.left_right)
                       
                        else:
                            self.data_pult['lx'] = 0

                    if event.axis == self.move_up_down:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_up_down:
                            self.data_pult['ry'] = int(round(event.value, 2) * self.up_down * -1)

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_up_down:
                            self.data_pult['ry'] = int(round(event.value, 2) * self.up_down)
                            
                        else:
                            self.data_pult['ry'] = 0

                    if event.axis == self.move_turn_left_turn_righ:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_turn_left_turn_righ:
                            self.data_pult['rx'] = int(round(event.value, 2) * self.turn_left_turn_righ * -1)

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_turn_left_turn_righ:
                            self.data_pult['rx'] = int(round(event.value, 2) * self.turn_left_turn_righ)
                            
                        else:
                            self.data_pult['rx'] = 0

                else:
                    self.data_pult['ly'], self.data_pult['ry'], self.data_pult['lx'], self.data_pult['rx'] = 0, 0, 0, 0

                # повторная инициализация джойстика после отключения
                joysticks = []
                for i in range(self.pygame.joystick.get_count()):
                    joysticks.append(self.pygame.joystick.Joystick(i))
                for self.joystick in joysticks:
                    self.joystick.init()
                    break

            # рассчет положения положения полезной нагрузки
            self.data_pult['servo_сam'] += cor_servo_cam
            
            # проверка на корректность значений 
            if self.data_pult['servo_сam'] >= self.max_value_cam:
                self.data_pult['servo_сam'] = self.max_value_cam

            elif self.data_pult['servo_сam'] <= self.min_value_cam:
                self.data_pult['servo_сam'] = self.min_value_cam

            QtCore.QThread.msleep(self.sleep_listen)

    def stop_listen(self):
        self.running = False

