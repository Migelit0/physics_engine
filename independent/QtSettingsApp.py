from PyQt5 import QtWidgets
import json

from core import get_config_dict
import design


class QtSettingsApp(QtWidgets.QMainWindow, design.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data = get_config_dict()

        self.k_slider.setValue(self.data['k_slider'])
        self.time_slider.setValue(self.data['time_slider'])
        self.mass_slider.setValue(self.data['mass_slider'])
        self.x_slider.setValue(self.data['x_slider'])
        self.y_slider.setValue(self.data['y_slider'])

        self.k_slider.valueChanged[int].connect(self.change_values)  # В ПРОЦЕНТАХ ВВОД ПАМАТУШТА ТАК УДОБНЕЙ
        self.time_slider.valueChanged[int].connect(self.change_values)
        self.mass_slider.valueChanged[int].connect(self.change_values)
        self.x_slider.valueChanged[int].connect(self.change_values)
        self.y_slider.valueChanged[int].connect(self.change_values)

        self.save_button.clicked.connect(self.save_json)
        self.color_button.clicked.connect(self.change_color)

    def change_values(self, value):  # записать во временный json файл значения всех слайдеров
        name = self.sender().objectName()
        self.data[name] = value

    def save_json(self):
        json_data = json.dumps(self.data)
        with open('temp/config.json', 'w') as file:
            file.write(json_data)

    def change_color(self):
        color = QtWidgets.QColorDialog.getColor()
        rgb = color.getRgb()
        color_list = [rgb[0], rgb[1], rgb[2]]  # генератор списков? не
        self.data['rgb'] = color_list
