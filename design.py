# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(467, 494)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(42, 11, 54, 16))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(134, 11, 53, 16))
        self.label_6.setObjectName("label_6")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(225, 11, 16, 436))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setSizeIncrement(QtCore.QSize(0, 0))
        self.line_2.setBaseSize(QtCore.QSize(0, 0))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(5)
        self.line_2.setMidLineWidth(0)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(266, 11, 36, 16))
        self.label_9.setObjectName("label_9")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(340, 11, 16, 16))
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(400, 11, 16, 16))
        self.label_10.setObjectName("label_10")
        self.mass_slider = QtWidgets.QSlider(Form)
        self.mass_slider.setGeometry(QtCore.QRect(266, 34, 22, 401))
        self.mass_slider.setMaximum(999999999)
        self.mass_slider.setProperty("value", 999999999)
        self.mass_slider.setOrientation(QtCore.Qt.Vertical)
        self.mass_slider.setObjectName("mass_slider")
        self.x_slider = QtWidgets.QSlider(Form)
        self.x_slider.setGeometry(QtCore.QRect(340, 34, 22, 401))
        self.x_slider.setMinimum(-5)
        self.x_slider.setMaximum(5)
        self.x_slider.setOrientation(QtCore.Qt.Vertical)
        self.x_slider.setObjectName("x_slider")
        self.y_slider = QtWidgets.QSlider(Form)
        self.y_slider.setGeometry(QtCore.QRect(400, 34, 22, 401))
        self.y_slider.setMinimum(-5)
        self.y_slider.setMaximum(5)
        self.y_slider.setOrientation(QtCore.Qt.Vertical)
        self.y_slider.setObjectName("y_slider")
        self.time_slider = QtWidgets.QSlider(Form)
        self.time_slider.setGeometry(QtCore.QRect(134, 34, 22, 401))
        self.time_slider.setMaximum(1000)
        self.time_slider.setProperty("value", 100)
        self.time_slider.setOrientation(QtCore.Qt.Vertical)
        self.time_slider.setObjectName("time_slider")
        self.k_slider = QtWidgets.QSlider(Form)
        self.k_slider.setGeometry(QtCore.QRect(42, 34, 22, 401))
        self.k_slider.setMinimum(0)
        self.k_slider.setMaximum(100)
        self.k_slider.setProperty("value", 100)
        self.k_slider.setOrientation(QtCore.Qt.Vertical)
        self.k_slider.setObjectName("k_slider")
        self.save_button = QtWidgets.QPushButton(Form)
        self.save_button.setGeometry(QtCore.QRect(42, 454, 93, 28))
        self.save_button.setObjectName("save_button")
        self.color_button = QtWidgets.QPushButton(Form)
        self.color_button.setGeometry(QtCore.QRect(266, 454, 93, 28))
        self.color_button.setObjectName("color_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_7.setText(_translate("Form", "КПД стен"))
        self.label_6.setText(_translate("Form", "Один тик"))
        self.label_9.setText(_translate("Form", "Масса"))
        self.label_8.setText(_translate("Form", "х"))
        self.label_10.setText(_translate("Form", "у"))
        self.save_button.setText(_translate("Form", "Сохранить"))
        self.color_button.setText(_translate("Form", "Выбрать цвет"))
