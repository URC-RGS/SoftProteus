import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from Design_debag_rov import*
from Rov_pult import * 


class ThreadServer(QtCore.QObject):
    commandserver = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.rov_pult_core = RovPost()

        # # словарик для отправки на аппарат
        # self.DataOutput = {'time': None,  # Текущее время
        #                    'motorpowervalue': 1,  # мощность моторов
        #                    'led': False,  # управление светом
        #                    'man': 90,  # Управление манипулятором
        #                    'servoCam': 90,  # управление наклоном камеры
        #                    'motor0': 0, 'motor1': 0,  # значения мощности на каждый мотор
        #                    'motor2': 0, 'motor3': 0,
        #                    'motor4': 0, 'motor5': 0}
        # # словарик получаемый с аппарата
        # self.DataInput = {'time': None, 'dept': None,
        #                   'volt': None, 'azimut': None}

        # self.deli = [1, 1, 1, 1]
        # self.lodi = MedaLogging()
        
        
        # self.Server = ServerPult(self.lodi, hostmod)  # поднимаем сервер
        # #self.lodi.info('ServerMainPult - init')

        # self.keboardjoi = MyControllerKeyboard()
        # self.DataPult = self.keboardjoi.DataPult

        # self.Controllps4 = MyController()  # поднимаем контролеер
        # self.DataPult = self.Controllps4.DataPult
        # self.Controllps4.deli = self.deli

        # self.RateCommandOut = 0.2
        # self.telemetria = False
        # self.cmdMod = False
        # self.checkKILL = False
        # self.correctCom = True

        # self.lodi.info('MainPost-init')


    def run(self):
        # основной цикл программы
        self.lodi.info('MainPost-RunCommand')

        def transformation(value: int):
            # Функция перевода значений АЦП с джойстика в проценты
            value = (32768 - value) // 655
            return value

        def defense(value: int):
            '''Функция защитник от некорректных данных'''
            if value > 100:
                value = 100
            elif value < 0:
                value = 0
            return value

        while True:
            # запрос данный из класса пульта (потенциально слабое место)
            data = self.DataPult

            # математика преобразования значений с джойстика в значения для моторов
            if self.telemetria:
                self.lodi.debug(f'DataPult - {data}')

            if self.correctCom:
                J1_Val_Y = transformation(data['j1-val-y']) + data['ly-cor']
                J1_Val_X = transformation(data['j1-val-x']) + data['lx-cor']
                J2_Val_Y = transformation(data['j2-val-y']) + data['ry-cor']
                J2_Val_X = transformation(data['j2-val-x']) + data['lx-cor']
            else:
                J1_Val_Y = transformation(data['j1-val-y'])
                J1_Val_X = transformation(data['j1-val-x'])
                J2_Val_Y = transformation(data['j2-val-y'])
                J2_Val_X = transformation(data['j2-val-x'])

            self.DataOutput['motor0'] = defense(
                J1_Val_Y + J1_Val_X + J2_Val_X - 100)
            self.DataOutput['motor1'] = defense(
                J1_Val_Y - J1_Val_X - J2_Val_X + 100)
            self.DataOutput['motor2'] = defense(
                (-1 * J1_Val_Y) - J1_Val_X + J2_Val_X + 100)
            self.DataOutput['motor3'] = defense(
                (-1 * J1_Val_Y) + J1_Val_X - J2_Val_X + 100)
            # Подготовка массива для отправки на аппарат
            self.DataOutput['motor4'] = defense(J2_Val_Y)
            self.DataOutput['motor5'] = defense(J2_Val_Y)

            self.DataOutput["time"] = str(datetime.now())

            self.DataOutput['led'] = data['led']
            self.DataOutput['man'] = data['man']
            self.DataOutput['servoCam'] = data['servoCam']
            # Запись управляющего массива в лог
            if self.telemetria:
                self.lodi.debug('DataOutput - {self.DataOutput}')
            # отправка и прием сообщений
            self.Server.ControlProteus(self.DataOutput)
            self.DataInput = self.Server.ReceiverProteus()
            datagui = self.DataInput
            datagui['log'] = self.DataOutput
            self.commandserver.emit(self.DataInput)

            # Запись принятого массива в лог
            if self.telemetria:
                self.lodi.debug('DataInput - {self.DataInput}')
            # возможность вывода принимаемой информации в соммандную строку
            if self.cmdMod:
                print(self.DataInput)
            # Проверка условия убийства сокета
            if self.checkKILL:
                self.Server.server.close()
                self.lodi.info('command-stop')
                break

            QtCore.QThread.msleep(250)


class ApplicationGUI(QMainWindow, DebagRovMainWindow):
    def __init__(self):
        # импорт и создание интерфейса
        super().__init__()
        self.setupUi(self)
       
        self.pushButton.clicked.connect(self.default)
        self.pushButton_2.clicked.connect(self.default)
        self.pushButton_3.clicked.connect(self.default)
        self.pushButton_4.clicked.connect(self.default)
        self.pushButton_5.clicked.connect(self.default)
        self.pushButton_6.clicked.connect(self.default)
        self.pushButton_7.clicked.connect(self.default)
        self.pushButton_8.clicked.connect(self.default)
        self.pushButton_9.clicked.connect(self.default)
        self.pushButton_10.clicked.connect(self.default)
        self.pushButton_11.clicked.connect(self.default)
        self.pushButton_12.clicked.connect(self.default)
        self.pushButton_13.clicked.connect(self.default)

        self.checkBox.stateChanged.connect(self.enebled)
        self.checkBox_2.stateChanged.connect(self.enebled)
        self.checkBox_3.stateChanged.connect(self.enebled)
        self.checkBox_4.stateChanged.connect(self.enebled)
        self.checkBox_5.stateChanged.connect(self.enebled)
        self.checkBox_6.stateChanged.connect(self.enebled)
        self.checkBox_7.stateChanged.connect(self.enebled)
        self.checkBox_8.stateChanged.connect(self.enebled)
        self.checkBox_9.stateChanged.connect(self.enebled)
        self.checkBox_10.stateChanged.connect(self.enebled)
        self.checkBox_11.stateChanged.connect(self.enebled)
        self.checkBox_12.stateChanged.connect(self.enebled)
        self.checkBox_13.stateChanged.connect(self.enebled)

        self.lcdNumber.display('-')
        self.lcdNumber_2.display('-')
        self.lcdNumber_3.display('-')
        self.lcdNumber_4.display('-')
        self.lcdNumber_5.display('-')
        self.lcdNumber_6.display('-')
        self.lcdNumber_7.display('-')
        self.lcdNumber_8.display('-')
        self.lcdNumber_9.display('-')
        self.lcdNumber_10.display('-')
        self.lcdNumber_11.display('-')
        self.lcdNumber_12.display('-')
        self.lcdNumber_13.display('-')
        
    def request(self):
        data = {}

        data['ly'] = self.verticalSlider.value()
        data['ry'] = self.verticalSlider_2.value()
        data['lx'] = self.horizontalSlider_10.value()
        data['rx'] = self.horizontalSlider_11.value()
        
        data['motor_0'] = self.horizontalSlider.value()
        data['motor_1'] = self.horizontalSlider_2.value()
        data['motor_2'] = self.horizontalSlider_3.value()
        data['motor_3'] = self.horizontalSlider_4.value()
        data['motor_4'] = self.horizontalSlider_5.value()
        data['motor_5'] = self.horizontalSlider_6.value()

        data['ser_cam'] = self.horizontalSlider_7.value()

        data['arm'] = self.horizontalSlider_8.value()

        data['led'] = self.horizontalSlider_9.value()

        return data

    def default(self):
        if self.sender() == self.pushButton_10:
            self.horizontalSlider_10.setValue(50)

        elif self.sender() == self.pushButton_11:
            self.verticalSlider.setValue(50)

        elif self.sender() == self.pushButton_12:
            self.horizontalSlider_11.setValue(50)

        elif self.sender() == self.pushButton_13:
            self.verticalSlider_2.setValue(50)

        elif self.sender() == self.pushButton:
            self.horizontalSlider.setValue(50)

        elif self.sender() == self.pushButton_2:
            self.horizontalSlider_2.setValue(50)

        elif self.sender() == self.pushButton_3:
            self.horizontalSlider_3.setValue(50)

        elif self.sender() == self.pushButton_4:
            self.horizontalSlider_4.setValue(50)

        elif self.sender() == self.pushButton_5:
            self.horizontalSlider_5.setValue(50)

        elif self.sender() == self.pushButton_6:
            self.horizontalSlider_6.setValue(50)

        elif self.sender() == self.pushButton_7:
            self.horizontalSlider_7.setValue(90)

        elif self.sender() == self.pushButton_8:
            self.horizontalSlider_8.setValue(0)

        elif self.sender() == self.pushButton_9:
            self.horizontalSlider_9.setValue(0)

    def enebled(self):

        if self.sender() == self.checkBox and self.checkBox.isChecked():
            self.lcdNumber.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(50)

        elif self.sender() == self.checkBox and not self.checkBox.isChecked():
            self.lcdNumber.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.horizontalSlider.setEnabled(False)
            self.horizontalSlider.setValue(50)

        elif self.sender() == self.checkBox_2 and self.checkBox_2.isChecked():
            self.lcdNumber_2.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.horizontalSlider_2.setEnabled(True)
            self.horizontalSlider_2.setValue(50)

        elif self.sender() == self.checkBox_2 and not self.checkBox_2.isChecked():
            self.lcdNumber_2.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.horizontalSlider_2.setEnabled(False)
            self.horizontalSlider_2.setValue(50)

        elif self.sender() == self.checkBox_3 and self.checkBox_3.isChecked():
            self.lcdNumber_3.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.horizontalSlider_3.setEnabled(True)
            self.horizontalSlider_3.setValue(50)

        elif self.sender() == self.checkBox_3 and not self.checkBox_3.isChecked():
            self.lcdNumber_3.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.horizontalSlider_3.setEnabled(False)
            self.horizontalSlider_3.setValue(50)

        elif self.sender() == self.checkBox_4 and self.checkBox_4.isChecked():
            self.lcdNumber_4.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.horizontalSlider_4.setEnabled(True)
            self.horizontalSlider_4.setValue(50)

        elif self.sender() == self.checkBox_4 and not self.checkBox_4.isChecked():
            self.lcdNumber_4.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.horizontalSlider_4.setEnabled(False)
            self.horizontalSlider_4.setValue(50)
            
        elif self.sender() == self.checkBox_5 and self.checkBox_5.isChecked():
            self.lcdNumber_5.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.horizontalSlider_5.setEnabled(True)
            self.horizontalSlider_5.setValue(50)

        elif self.sender() == self.checkBox_5 and not self.checkBox_5.isChecked():
            self.lcdNumber_5.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.horizontalSlider_5.setEnabled(False)
            self.horizontalSlider_5.setValue(50)

        elif self.sender() == self.checkBox_6 and self.checkBox_6.isChecked():
            self.lcdNumber_6.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.horizontalSlider_6.setEnabled(True)
            self.horizontalSlider_6.setValue(50)

        elif self.sender() == self.checkBox_6 and not self.checkBox_6.isChecked():
            self.lcdNumber_6.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.horizontalSlider_6.setEnabled(False)
            self.horizontalSlider_6.setValue(50)

        elif self.sender() == self.checkBox_7 and self.checkBox_7.isChecked():
            self.lcdNumber_7.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.horizontalSlider_7.setEnabled(True)
            self.horizontalSlider_7.setValue(90)

        elif self.sender() == self.checkBox_7 and not self.checkBox_7.isChecked():
            self.lcdNumber_7.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            self.horizontalSlider_7.setEnabled(False)
            self.horizontalSlider_7.setValue(90)

        elif self.sender() == self.checkBox_8 and self.checkBox_8.isChecked():
            self.lcdNumber_8.setEnabled(True)
            self.pushButton_8.setEnabled(True)
            self.horizontalSlider_8.setEnabled(True)
            self.horizontalSlider_8.setValue(0)

        elif self.sender() == self.checkBox_8 and not self.checkBox_8.isChecked():
            self.lcdNumber_8.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            self.horizontalSlider_8.setEnabled(False)
            self.horizontalSlider_8.setValue(0)

        elif self.sender() == self.checkBox_9 and self.checkBox_9.isChecked():
            self.lcdNumber_9.setEnabled(True)
            self.pushButton_9.setEnabled(True)
            self.horizontalSlider_9.setEnabled(True)
            self.horizontalSlider_9.setValue(0)

        elif self.sender() == self.checkBox_9 and not self.checkBox_9.isChecked():
            self.lcdNumber_9.setEnabled(False)
            self.pushButton_9.setEnabled(False)
            self.horizontalSlider_9.setEnabled(False)
            self.horizontalSlider_9.setValue(0)

        elif self.sender() == self.checkBox_12 and self.checkBox_12.isChecked():
            self.pushButton_10.setEnabled(True)
            self.horizontalSlider_10.setEnabled(True)
            self.horizontalSlider_10.setValue(50)

        elif self.sender() == self.checkBox_12 and not self.checkBox_12.isChecked():
            self.pushButton_10.setEnabled(False)
            self.horizontalSlider_10.setEnabled(False)
            self.horizontalSlider_10.setValue(50)

        elif self.sender() == self.checkBox_10 and self.checkBox_10.isChecked():
            self.pushButton_11.setEnabled(True)
            self.verticalSlider.setEnabled(True)
            self.verticalSlider.setValue(50)

        elif self.sender() == self.checkBox_10 and not self.checkBox_10.isChecked():
            self.pushButton_11.setEnabled(False)
            self.verticalSlider.setEnabled(False)
            self.verticalSlider.setValue(50)

        elif self.sender() == self.checkBox_13 and self.checkBox_13.isChecked():
            self.pushButton_12.setEnabled(True)
            self.horizontalSlider_11.setEnabled(True)
            self.horizontalSlider_11.setValue(50)

        elif self.sender() == self.checkBox_13 and not self.checkBox_13.isChecked():
            self.pushButton_12.setEnabled(False)
            self.horizontalSlider_11.setEnabled(False)
            self.horizontalSlider_11.setValue(50)

        elif self.sender() == self.checkBox_11 and self.checkBox_11.isChecked():
            self.pushButton_13.setEnabled(True)
            self.verticalSlider_2.setEnabled(True)
            self.verticalSlider_2.setValue(50)

        elif self.sender() == self.checkBox_11 and not self.checkBox_11.isChecked():
            self.pushButton_13.setEnabled(False)
            self.verticalSlider_2.setEnabled(False)
            self.verticalSlider_2.setValue(50)

    def start_server(self):
        # запуск сервера
        
        # self.check_connect = True
        # self.threadserver = ThreadServer(self.modeHost)
        # self.threadserver.moveToThread(self.thread)
        # self.threadserver.commandserver.connect(self.updategui)
        # self.thread.started.connect(self.threadserver.run)
        # self.textBrowser.append('### Connecting ###')
        # self.thread.start()
        pass

    def start_joi(self):
        # self.threadJoi = threading.Thread(
        #     target=self.threadserver.RunController)
        # self.threadJoi.start()
        pass

    def close_event(self, e):
        # диалоговое окошко закрытия
        result = QtWidgets.QMessageBox.question(self, "Подтверждение закрытия окна",
                                                      "Вы действительно хотите закрыть окно?",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            e.accept()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()

    def updategui(self, data):
        try:
            # обновление интерфейса
            # напряжение
            self.lcdNumber_11.display()
            # ток 
            self.lcdNumber_10.display()
            # глубина
            self.lcdNumber_12.display()
            # курс
            self.lcdNumber_13.display()
            # ток с моторов 
            # 0
            self.lcdNumber.display()
            # 1
            self.lcdNumber_2.display()
            # 2
            self.lcdNumber_3.display()
            # 3
            self.lcdNumber_4.display()
            # 4
            self.lcdNumber_5.display()
            # 5
            self.lcdNumber_6.display()
            # ser_cam
            self.lcdNumber_7.display()
            # arm
            self.lcdNumber_8.display()
            # led
            self.lcdNumber_9.display()

            return True

        except:
            return False



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApplicationGUI()
    ex.show()
    sys.exit(app.exec_())