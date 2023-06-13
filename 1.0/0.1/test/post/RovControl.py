import os
import pygame
from time import sleep


class RovController():
    def __init__(self, config):

        os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.pygame = pygame
        self.pygame.init()

        self.config = config

        joysticks = []
        for i in range(self.pygame.joystick.get_count()):
            joysticks.append(self.pygame.joystick.Joystick(i))
        for self.joystick in joysticks:
            self.joystick.init()

        self.DataPult = {'j1-val-y': 0, 'j1-val-x': 0,
                         'j2-val-y': 0, 'j2-val-x': 0,
                         'man': 90, 'servoCam': 90,
                         'led': 0}

        self.camera_up = int(self.config['JOYSTICK'][self.config['JOYSTICK']['camera_up']])

        self.camera_down = int(self.config['JOYSTICK'][self.config['JOYSTICK']['camera_down']])

        self.arm_up =  int(self.config['JOYSTICK'][self.config['JOYSTICK']['arm_up']])

        self.arm_down =  int(self.config['JOYSTICK'][self.config['JOYSTICK']['arm_down']])

        self.led_up = int(self.config['JOYSTICK'][self.config['JOYSTICK']['led_up']])

        self.led_down = int(self.config['JOYSTICK'][self.config['JOYSTICK']['led_down']])

        self.sleep_listen = float(self.config['JOYSTICK']['time_sleep'])

        self.power_motor = float(self.config['JOYSTICK']['power_motor'])

        self.forward_back_defolt = float(self.config['JOYSTICK']['forward_back_defolt']) * self.power_motor * 32767

        self.cor_forward_back_defolt = float(self.config['JOYSTICK']['cor_forward_back_defolt'])

        self.min_value = float(self.config['JOYSTICK']['min_value'])

        self.move_forward_back = int(self.config['JOYSTICK'][self.config['JOYSTICK']['move_forward_back']])

        self.left_right_defolt = float(self.config['JOYSTICK']['left_right_defolt']) * self.power_motor * 32767

        self.cor_left_right_defolt = float(self.config['JOYSTICK']['cor_left_right_defolt'])

        self.move_left_right = int(self.config['JOYSTICK'][self.config['JOYSTICK']['move_left_right']])

        self.move_up_down = int(self.config['JOYSTICK'][self.config['JOYSTICK']['move_up_down']])

        self.up_down_defolt = float(self.config['JOYSTICK']['up_down_defolt']) * self.power_motor * 32767

        self.cor_up_down_defolt = float(self.config['JOYSTICK']['cor_up_down_defolt'])

        self.move_turn_left_turn_righ = int(self.config['JOYSTICK'][self.config['JOYSTICK']['move_turn-left_turn-righ']])

        self.turn_left_turn_righ_defolt = float(self.config['JOYSTICK']['turn-left_turn-righ_defolt']) * self.power_motor * 32767

        self.cor_turn_left_turn_righ_defolt = float(self.config['JOYSTICK']['cor_turn-left_turn-righ_defolt'])

        self.running = True

    def listen(self):
        cor_servo_cam = 0
        while self.running:
            for event in self.pygame.event.get():
                # опрос нажания кнопок
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == self.camera_up:
                        cor_servo_cam = 1

                    if event.button == self.camera_down:
                        cor_servo_cam = -1

                    if event.button == self.arm_up:
                        self.DataPult['man'] = 180

                    if event.button == self.arm_down:
                        self.DataPult['man'] = 0

                    if event.button == self.led_up:
                        self.DataPult['led'] = 1

                    if event.button == self.led_down:
                        self.DataPult['led'] = 0

                if event.type == pygame.JOYBUTTONUP:
                    if event.button == self.camera_up:
                        cor_servo_cam = 0

                    if event.button == self.camera_down:
                        cor_servo_cam = 0

                # опрос стиков
                if event.type == pygame.JOYAXISMOTION and abs(event.value) > self.min_value:
                    if event.axis == self.move_forward_back:
                        self.DataPult['j1-val-y'] = int(round(event.value, 2) * self.forward_back_defolt) - self.cor_forward_back_defolt

                    if event.axis == self.move_left_right:
                        self.DataPult['j1-val-x'] = int(round(event.value, 2) * self.left_right_defolt) - self.cor_left_right_defolt

                    if event.axis == self.move_up_down:
                        self.DataPult['j2-val-y'] = int(round(event.value, 2) * self.up_down_defolt) - self.cor_up_down_defolt

                    if event.axis == self.move_turn_left_turn_righ:
                        self.DataPult['j2-val-x'] = int(round(event.value, 2) * self.turn_left_turn_righ_defolt) - self.cor_turn_left_turn_righ_defolt
                else:
                    self.DataPult['j1-val-y'], self.DataPult['j2-val-y'], self.DataPult['j1-val-x'], self.DataPult['j2-val-x'] = 0, 0, 0, 0

                # повторная инициализация джойстика после отключения
                
                joysticks = []
                for i in range(self.pygame.joystick.get_count()):
                    joysticks.append(self.pygame.joystick.Joystick(i))
                for self.joystick in joysticks:
                    self.joystick.init()
                    break

            # рассчет положения положения полезной нагрузки
            self.DataPult['servoCam'] += cor_servo_cam
            if self.DataPult['servoCam'] > 180:
                self.DataPult['servoCam'] = 180
            elif self.DataPult['servoCam'] < 0:
                self.DataPult['servoCam'] = 0

            sleep(float(self.config['JOYSTICK']['time_sleep']))

    def stop_listen(self):
        self.running = False

