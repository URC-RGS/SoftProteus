# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designJeraih.ui'
##
## Created by: Qt User Interface Compiler version 5.15.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UpperPCGUI(object):
    def setupUi(self, UpperPCGUI):
        if not UpperPCGUI.objectName():
            UpperPCGUI.setObjectName(u"UpperPCGUI")
        UpperPCGUI.resize(1075, 483)
        UpperPCGUI.setMinimumSize(QSize(900, 0))
        self.centralwidget = QWidget(UpperPCGUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 20))
        self.tabWidget.setSizeIncrement(QSize(0, 20))
        self.tabWidget.setStyleSheet(u"color=rgb(0, 170, 255)")
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.Main = QWidget()
        self.Main.setObjectName(u"Main")
        self.gridLayout_2 = QGridLayout(self.Main)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.temp_label = QLabel(self.Main)
        self.temp_label.setObjectName(u"temp_label")
        self.temp_label.setLayoutDirection(Qt.LeftToRight)
        self.temp_label.setTextFormat(Qt.AutoText)
        self.temp_label.setScaledContents(False)
        self.temp_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.temp_label)

        self.term_value = QLCDNumber(self.Main)
        self.term_value.setObjectName(u"term_value")
        self.term_value.setSmallDecimalPoint(False)

        self.horizontalLayout.addWidget(self.term_value)

        self.depth_label = QLabel(self.Main)
        self.depth_label.setObjectName(u"depth_label")
        self.depth_label.setTextFormat(Qt.RichText)
        self.depth_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.depth_label)

        self.depth_value = QLCDNumber(self.Main)
        self.depth_value.setObjectName(u"depth_value")

        self.horizontalLayout.addWidget(self.depth_value)

        self.orientation_label = QLabel(self.Main)
        self.orientation_label.setObjectName(u"orientation_label")
        self.orientation_label.setTextFormat(Qt.RichText)
        self.orientation_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.orientation_label.setWordWrap(False)
        self.orientation_label.setMargin(1)

        self.horizontalLayout.addWidget(self.orientation_label)

        self.orientation_value = QLCDNumber(self.Main)
        self.orientation_value.setObjectName(u"orientation_value")

        self.horizontalLayout.addWidget(self.orientation_value)


        self.gridLayout_2.addLayout(self.horizontalLayout, 6, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.angle_x_label = QLabel(self.Main)
        self.angle_x_label.setObjectName(u"angle_x_label")

        self.horizontalLayout_3.addWidget(self.angle_x_label)

        self.angle_x_value = QLCDNumber(self.Main)
        self.angle_x_value.setObjectName(u"angle_x_value")

        self.horizontalLayout_3.addWidget(self.angle_x_value)

        self.angle_y_label = QLabel(self.Main)
        self.angle_y_label.setObjectName(u"angle_y_label")

        self.horizontalLayout_3.addWidget(self.angle_y_label)

        self.angle_y_value = QLCDNumber(self.Main)
        self.angle_y_value.setObjectName(u"angle_y_value")

        self.horizontalLayout_3.addWidget(self.angle_y_value)

        self.angle_z_label = QLabel(self.Main)
        self.angle_z_label.setObjectName(u"angle_z_label")

        self.horizontalLayout_3.addWidget(self.angle_z_label)

        self.angle_z_value = QLCDNumber(self.Main)
        self.angle_z_value.setObjectName(u"angle_z_value")

        self.horizontalLayout_3.addWidget(self.angle_z_value)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 8, 0, 1, 1)

        self.line_1 = QFrame(self.Main)
        self.line_1.setObjectName(u"line_1")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.line_1.sizePolicy().hasHeightForWidth())
        self.line_1.setSizePolicy(sizePolicy)
        self.line_1.setStyleSheet(u"color:rgb(0, 170, 255)")
        self.line_1.setLineWidth(10)
        self.line_1.setMidLineWidth(10)
        self.line_1.setFrameShape(QFrame.HLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_1, 9, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.amperage_label = QLabel(self.Main)
        self.amperage_label.setObjectName(u"amperage_label")

        self.horizontalLayout_2.addWidget(self.amperage_label)

        self.amperage_value = QLCDNumber(self.Main)
        self.amperage_value.setObjectName(u"amperage_value")

        self.horizontalLayout_2.addWidget(self.amperage_value)

        self.voltage_label = QLabel(self.Main)
        self.voltage_label.setObjectName(u"voltage_label")

        self.horizontalLayout_2.addWidget(self.voltage_label)

        self.voltage_value = QLCDNumber(self.Main)
        self.voltage_value.setObjectName(u"voltage_value")

        self.horizontalLayout_2.addWidget(self.voltage_value)

        self.charge_label = QLabel(self.Main)
        self.charge_label.setObjectName(u"charge_label")

        self.horizontalLayout_2.addWidget(self.charge_label)

        self.charge_value = QLCDNumber(self.Main)
        self.charge_value.setObjectName(u"charge_value")

        self.horizontalLayout_2.addWidget(self.charge_value)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 10, 0, 1, 1)

        self.line_0 = QFrame(self.Main)
        self.line_0.setObjectName(u"line_0")
        self.line_0.setEnabled(True)
        self.line_0.setMinimumSize(QSize(0, 0))
        self.line_0.setSizeIncrement(QSize(0, 0))
        self.line_0.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.line_0.setFont(font)
        self.line_0.setStyleSheet(u"color:rgb(0, 170, 255)")
        self.line_0.setFrameShadow(QFrame.Sunken)
        self.line_0.setFrameShape(QFrame.HLine)

        self.gridLayout_2.addWidget(self.line_0, 7, 0, 1, 1)

        self.tabWidget.addTab(self.Main, "")
        self.Settings = QWidget()
        self.Settings.setObjectName(u"Settings")
        self.gridLayout = QGridLayout(self.Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.button_connect = QPushButton(self.Settings)
        self.button_connect.setObjectName(u"button_connect")

        self.horizontalLayout_11.addWidget(self.button_connect)


        self.gridLayout.addLayout(self.horizontalLayout_11, 9, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.cam_up_label = QLabel(self.Settings)
        self.cam_up_label.setObjectName(u"cam_up_label")

        self.horizontalLayout_7.addWidget(self.cam_up_label)

        self.camera_up_set = QComboBox(self.Settings)
        self.camera_up_set.addItem("")
        self.camera_up_set.addItem("")
        self.camera_up_set.addItem("")
        self.camera_up_set.addItem("")
        self.camera_up_set.addItem("")
        self.camera_up_set.addItem("")
        self.camera_up_set.addItem("")
        self.camera_up_set.addItem("")
        self.camera_up_set.setObjectName(u"camera_up_set")

        self.horizontalLayout_7.addWidget(self.camera_up_set)

        self.camera_down_label = QLabel(self.Settings)
        self.camera_down_label.setObjectName(u"camera_down_label")

        self.horizontalLayout_7.addWidget(self.camera_down_label)

        self.camera_dowm_set = QComboBox(self.Settings)
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.addItem("")
        self.camera_dowm_set.setObjectName(u"camera_dowm_set")

        self.horizontalLayout_7.addWidget(self.camera_dowm_set)


        self.gridLayout.addLayout(self.horizontalLayout_7, 2, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.host_label = QLabel(self.Settings)
        self.host_label.setObjectName(u"host_label")

        self.horizontalLayout_8.addWidget(self.host_label)

        self.host_value = QLineEdit(self.Settings)
        self.host_value.setObjectName(u"host_value")

        self.horizontalLayout_8.addWidget(self.host_value)

        self.port_label = QLabel(self.Settings)
        self.port_label.setObjectName(u"port_label")

        self.horizontalLayout_8.addWidget(self.port_label)

        self.port_value = QLineEdit(self.Settings)
        self.port_value.setObjectName(u"port_value")

        self.horizontalLayout_8.addWidget(self.port_value)


        self.gridLayout.addLayout(self.horizontalLayout_8, 6, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.l_r_label = QLabel(self.Settings)
        self.l_r_label.setObjectName(u"l_r_label")
        self.l_r_label.setTextFormat(Qt.RichText)

        self.horizontalLayout_6.addWidget(self.l_r_label)

        self.l_r_set = QComboBox(self.Settings)
        self.l_r_set.addItem("")
        self.l_r_set.addItem("")
        self.l_r_set.addItem("")
        self.l_r_set.addItem("")
        self.l_r_set.setObjectName(u"l_r_set")

        self.horizontalLayout_6.addWidget(self.l_r_set)

        self.l_r_value = QDoubleSpinBox(self.Settings)
        self.l_r_value.setObjectName(u"l_r_value")
        self.l_r_value.setMinimum(-1.000000000000000)
        self.l_r_value.setMaximum(1.000000000000000)
        self.l_r_value.setSingleStep(0.050000000000000)
        self.l_r_value.setValue(1.000000000000000)

        self.horizontalLayout_6.addWidget(self.l_r_value)

        self.tl_tr_label = QLabel(self.Settings)
        self.tl_tr_label.setObjectName(u"tl_tr_label")

        self.horizontalLayout_6.addWidget(self.tl_tr_label)

        self.tl_tr_set = QComboBox(self.Settings)
        self.tl_tr_set.addItem("")
        self.tl_tr_set.addItem("")
        self.tl_tr_set.addItem("")
        self.tl_tr_set.addItem("")
        self.tl_tr_set.setObjectName(u"tl_tr_set")

        self.horizontalLayout_6.addWidget(self.tl_tr_set)

        self.tl_tr_value = QDoubleSpinBox(self.Settings)
        self.tl_tr_value.setObjectName(u"tl_tr_value")
        self.tl_tr_value.setMinimum(-1.000000000000000)
        self.tl_tr_value.setMaximum(1.000000000000000)
        self.tl_tr_value.setSingleStep(0.050000000000000)
        self.tl_tr_value.setValue(1.000000000000000)

        self.horizontalLayout_6.addWidget(self.tl_tr_value)


        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.f_b_label = QLabel(self.Settings)
        self.f_b_label.setObjectName(u"f_b_label")
        self.f_b_label.setTextFormat(Qt.RichText)

        self.horizontalLayout_5.addWidget(self.f_b_label)

        self.f_b_set = QComboBox(self.Settings)
        self.f_b_set.addItem("")
        self.f_b_set.addItem("")
        self.f_b_set.addItem("")
        self.f_b_set.addItem("")
        self.f_b_set.setObjectName(u"f_b_set")

        self.horizontalLayout_5.addWidget(self.f_b_set)

        self.f_b_value = QDoubleSpinBox(self.Settings)
        self.f_b_value.setObjectName(u"f_b_value")
        self.f_b_value.setMinimum(-1.000000000000000)
        self.f_b_value.setMaximum(1.000000000000000)
        self.f_b_value.setSingleStep(0.050000000000000)
        self.f_b_value.setValue(1.000000000000000)

        self.horizontalLayout_5.addWidget(self.f_b_value)

        self.u_d_label = QLabel(self.Settings)
        self.u_d_label.setObjectName(u"u_d_label")
        self.u_d_label.setTextFormat(Qt.RichText)

        self.horizontalLayout_5.addWidget(self.u_d_label)

        self.u_d_set = QComboBox(self.Settings)
        self.u_d_set.addItem("")
        self.u_d_set.addItem("")
        self.u_d_set.addItem("")
        self.u_d_set.addItem("")
        self.u_d_set.setObjectName(u"u_d_set")

        self.horizontalLayout_5.addWidget(self.u_d_set)

        self.u_d_value = QDoubleSpinBox(self.Settings)
        self.u_d_value.setObjectName(u"u_d_value")
        self.u_d_value.setMinimum(-1.000000000000000)
        self.u_d_value.setMaximum(1.000000000000000)
        self.u_d_value.setSingleStep(0.050000000000000)
        self.u_d_value.setValue(1.000000000000000)

        self.horizontalLayout_5.addWidget(self.u_d_value)


        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.led_on_label = QLabel(self.Settings)
        self.led_on_label.setObjectName(u"led_on_label")

        self.horizontalLayout_10.addWidget(self.led_on_label)

        self.led_on_set = QComboBox(self.Settings)
        self.led_on_set.addItem("")
        self.led_on_set.addItem("")
        self.led_on_set.addItem("")
        self.led_on_set.addItem("")
        self.led_on_set.addItem("")
        self.led_on_set.addItem("")
        self.led_on_set.addItem("")
        self.led_on_set.addItem("")
        self.led_on_set.setObjectName(u"led_on_set")

        self.horizontalLayout_10.addWidget(self.led_on_set)

        self.led_off_label = QLabel(self.Settings)
        self.led_off_label.setObjectName(u"led_off_label")

        self.horizontalLayout_10.addWidget(self.led_off_label)

        self.led_off_set = QComboBox(self.Settings)
        self.led_off_set.addItem("")
        self.led_off_set.addItem("")
        self.led_off_set.addItem("")
        self.led_off_set.addItem("")
        self.led_off_set.addItem("")
        self.led_off_set.addItem("")
        self.led_off_set.addItem("")
        self.led_off_set.addItem("")
        self.led_off_set.setObjectName(u"led_off_set")

        self.horizontalLayout_10.addWidget(self.led_off_set)


        self.gridLayout.addLayout(self.horizontalLayout_10, 4, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.arm_up_label = QLabel(self.Settings)
        self.arm_up_label.setObjectName(u"arm_up_label")

        self.horizontalLayout_9.addWidget(self.arm_up_label)

        self.arm_up_set = QComboBox(self.Settings)
        self.arm_up_set.addItem("")
        self.arm_up_set.addItem("")
        self.arm_up_set.addItem("")
        self.arm_up_set.addItem("")
        self.arm_up_set.addItem("")
        self.arm_up_set.addItem("")
        self.arm_up_set.addItem("")
        self.arm_up_set.addItem("")
        self.arm_up_set.setObjectName(u"arm_up_set")

        self.horizontalLayout_9.addWidget(self.arm_up_set)

        self.arm_down_label = QLabel(self.Settings)
        self.arm_down_label.setObjectName(u"arm_down_label")

        self.horizontalLayout_9.addWidget(self.arm_down_label)

        self.arm_down_set = QComboBox(self.Settings)
        self.arm_down_set.addItem("")
        self.arm_down_set.addItem("")
        self.arm_down_set.addItem("")
        self.arm_down_set.addItem("")
        self.arm_down_set.addItem("")
        self.arm_down_set.addItem("")
        self.arm_down_set.addItem("")
        self.arm_down_set.addItem("")
        self.arm_down_set.setObjectName(u"arm_down_set")

        self.horizontalLayout_9.addWidget(self.arm_down_set)


        self.gridLayout.addLayout(self.horizontalLayout_9, 3, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.button_apply = QPushButton(self.Settings)
        self.button_apply.setObjectName(u"button_apply")

        self.horizontalLayout_12.addWidget(self.button_apply)


        self.gridLayout.addLayout(self.horizontalLayout_12, 5, 0, 1, 1)

        self.tabWidget.addTab(self.Settings, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 1, 1, 1)

        UpperPCGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(UpperPCGUI)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(UpperPCGUI)
    # setupUi

    def retranslateUi(self, UpperPCGUI):
        UpperPCGUI.setWindowTitle(QCoreApplication.translate("UpperPCGUI", u"UpperPCGUI", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("UpperPCGUI", u"<span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">", None))
#endif // QT_CONFIG(tooltip)
        self.temp_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Term</span></p></body></html>", None))
        self.depth_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Depth</span></p></body></html>", None))
        self.orientation_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Orientation</span></p></body></html>", None))
        self.angle_x_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Angle X</span></p></body></html>", None))
        self.angle_y_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Angle Y</span></p></body></html>", None))
        self.angle_z_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Angle Z</span></p></body></html>", None))
        self.amperage_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Amperage</span></p></body></html>", None))
        self.voltage_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">Voltage</span></p></body></html>", None))
        self.charge_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600; color:#00aaff;\">\u0421harge</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Main), QCoreApplication.translate("UpperPCGUI", u"Main", None))
        self.button_connect.setText(QCoreApplication.translate("UpperPCGUI", u"Connect", None))
        self.cam_up_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Camera Up", None))
        self.camera_up_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"circle", None))
        self.camera_up_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"square", None))
        self.camera_up_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"triangle", None))
        self.camera_up_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"x", None))
        self.camera_up_set.setItemText(4, QCoreApplication.translate("UpperPCGUI", u"l1", None))
        self.camera_up_set.setItemText(5, QCoreApplication.translate("UpperPCGUI", u"l2", None))
        self.camera_up_set.setItemText(6, QCoreApplication.translate("UpperPCGUI", u"r1", None))
        self.camera_up_set.setItemText(7, QCoreApplication.translate("UpperPCGUI", u"r2", None))

        self.camera_down_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Camera Down", None))
        self.camera_dowm_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"circle", None))
        self.camera_dowm_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"square", None))
        self.camera_dowm_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"triangle", None))
        self.camera_dowm_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"x", None))
        self.camera_dowm_set.setItemText(4, QCoreApplication.translate("UpperPCGUI", u"l1", None))
        self.camera_dowm_set.setItemText(5, QCoreApplication.translate("UpperPCGUI", u"l2", None))
        self.camera_dowm_set.setItemText(6, QCoreApplication.translate("UpperPCGUI", u"r1", None))
        self.camera_dowm_set.setItemText(7, QCoreApplication.translate("UpperPCGUI", u"r2", None))

        self.host_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">HOST</span></p></body></html>", None))
        self.host_value.setText(QCoreApplication.translate("UpperPCGUI", u"127.0.0.1", None))
        self.port_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">PORT</span></p></body></html>", None))
        self.port_value.setText(QCoreApplication.translate("UpperPCGUI", u"3000", None))
        self.l_r_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Left \\ Right</span></p></body></html>", None))
        self.l_r_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"lx", None))
        self.l_r_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"ly", None))
        self.l_r_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"rx", None))
        self.l_r_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"ry", None))

        self.tl_tr_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Turn left \\ Turn righ</span></p></body></html>", None))
        self.tl_tr_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"lx", None))
        self.tl_tr_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"ly", None))
        self.tl_tr_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"rx", None))
        self.tl_tr_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"ry", None))

        self.f_b_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Forward \\ Back</span></p></body></html>", None))
        self.f_b_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"lx", None))
        self.f_b_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"ly", None))
        self.f_b_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"rx", None))
        self.f_b_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"ry", None))

        self.f_b_set.setPlaceholderText("")
        self.u_d_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Up \\ Down</span></p></body></html>", None))
        self.u_d_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"lx", None))
        self.u_d_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"ly", None))
        self.u_d_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"rx", None))
        self.u_d_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"ry", None))

        self.led_on_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Led On", None))
        self.led_on_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"circle", None))
        self.led_on_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"square", None))
        self.led_on_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"triangle", None))
        self.led_on_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"x", None))
        self.led_on_set.setItemText(4, QCoreApplication.translate("UpperPCGUI", u"l1", None))
        self.led_on_set.setItemText(5, QCoreApplication.translate("UpperPCGUI", u"l2", None))
        self.led_on_set.setItemText(6, QCoreApplication.translate("UpperPCGUI", u"r1", None))
        self.led_on_set.setItemText(7, QCoreApplication.translate("UpperPCGUI", u"r2", None))

        self.led_off_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Led Off", None))
        self.led_off_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"circle", None))
        self.led_off_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"square ", None))
        self.led_off_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"triangle", None))
        self.led_off_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"x", None))
        self.led_off_set.setItemText(4, QCoreApplication.translate("UpperPCGUI", u"l1", None))
        self.led_off_set.setItemText(5, QCoreApplication.translate("UpperPCGUI", u"l2", None))
        self.led_off_set.setItemText(6, QCoreApplication.translate("UpperPCGUI", u"r1", None))
        self.led_off_set.setItemText(7, QCoreApplication.translate("UpperPCGUI", u"r2", None))

        self.arm_up_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Arm Up", None))
        self.arm_up_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"circle", None))
        self.arm_up_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"square", None))
        self.arm_up_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"triangle", None))
        self.arm_up_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"x", None))
        self.arm_up_set.setItemText(4, QCoreApplication.translate("UpperPCGUI", u"l1", None))
        self.arm_up_set.setItemText(5, QCoreApplication.translate("UpperPCGUI", u"l2", None))
        self.arm_up_set.setItemText(6, QCoreApplication.translate("UpperPCGUI", u"r1", None))
        self.arm_up_set.setItemText(7, QCoreApplication.translate("UpperPCGUI", u"r2", None))

        self.arm_down_label.setText(QCoreApplication.translate("UpperPCGUI", u"<html><head/><body><p align=\"right\"><span style=\" font-size:12pt; font-weight:600; color:#00aaff;\">Arm Down", None))
        self.arm_down_set.setItemText(0, QCoreApplication.translate("UpperPCGUI", u"circle", None))
        self.arm_down_set.setItemText(1, QCoreApplication.translate("UpperPCGUI", u"square", None))
        self.arm_down_set.setItemText(2, QCoreApplication.translate("UpperPCGUI", u"triangle", None))
        self.arm_down_set.setItemText(3, QCoreApplication.translate("UpperPCGUI", u"x", None))
        self.arm_down_set.setItemText(4, QCoreApplication.translate("UpperPCGUI", u"l1", None))
        self.arm_down_set.setItemText(5, QCoreApplication.translate("UpperPCGUI", u"l2", None))
        self.arm_down_set.setItemText(6, QCoreApplication.translate("UpperPCGUI", u"r1", None))
        self.arm_down_set.setItemText(7, QCoreApplication.translate("UpperPCGUI", u"r2", None))

        self.button_apply.setText(QCoreApplication.translate("UpperPCGUI", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Settings), QCoreApplication.translate("UpperPCGUI", u"Settings", None))
    # retranslateUi

