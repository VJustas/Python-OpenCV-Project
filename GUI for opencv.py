#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import os

from PySide.QtGui import *
from PySide.QtCore import *

from utilities import *
import controller

class QFrameEfekto1(QFrame):
    def __init__(self, parent = None):
        super(QFrameEfekto1, self).__init__(parent)

        self.name = 'Effect1'
        control.set_effect_to_control(self.name)

        self.start_stop_button = QPushButton(text = "Start")

        grid = QGridLayout()
        grid.addWidget(self.start_stop_button, 1, 0)
        self.setLayout(grid)

        self.connect(self.start_stop_button, SIGNAL("clicked()"), self.start_stop_pressed)

    def start_stop_pressed(self):
        if self.start_stop_button.text() == "Start":
            self.start_stop_button.setText("Cancel")
            control.start()
        else:
            self.start_stop_button.setText("Start")
            control.stop()


class QFrameEfekto2(QFrame):
    def __init__(self, parent = None):
        super(QFrameEfekto2, self).__init__(parent)
        
        self.name = 'Effect2'
        control.set_effect_to_control(self.name)

        #Radio buttons
        self.normal_radio_button = QRadioButton(text = "No filter")
        self.grey_radio_button = QRadioButton(text = "Greyscale")
        self.sepia_radio_button = QRadioButton(text = "Sepia")

        filtro_radio_buttons = QGroupBox('Filters')

        vbox = QVBoxLayout()
        vbox.addWidget(self.normal_radio_button)
        vbox.addWidget(self.grey_radio_button)
        vbox.addWidget(self.sepia_radio_button)

        filtro_radio_buttons.setLayout(vbox)

        self.normal_radio_button.setChecked(True)

        #Buttons
        self.start_stop_button = QPushButton(text = "Start")

        #Spinbox and Dial
        self.checkbox = QCheckBox(text = u"Enable")
        self.dial = QDial() #kinda like speedometer of car
        self.dial.setNotchesVisible(True)
        self.dial.setMaximum(30)

        self.spinbox = QSpinBox()
        self.spinbox.setMaximum(30)

        layout_dial = QHBoxLayout()
        layout_dial.addWidget(self.checkbox)
        layout_dial.addWidget(self.dial)
        layout_dial.addWidget(self.spinbox)  
        gaussian_blur = QGroupBox('Gaussian blur')
        gaussian_blur.setLayout(layout_dial)    

        #watermark
        self.watermark_checkbox = QCheckBox(text = u"Enable")
        self.watermark_checkbox.setChecked(True)
        watermark_layout = QHBoxLayout()
        watermark_layout.addWidget(self.watermark_checkbox)
        watermark = QGroupBox('Logo')
        watermark.setLayout(watermark_layout)

        grid = QGridLayout()

        grid.addWidget(filtro_radio_buttons, 0, 0)
        grid.addWidget(gaussian_blur, 1, 0)
        grid.addWidget(watermark, 2, 0)
        grid.addWidget(self.start_stop_button, 3, 0)

        self.setLayout(grid)

        self.connect(self.start_stop_button, SIGNAL("clicked()"), self.start_stop_pressed)

        self.connect(self.grey_radio_button, SIGNAL("pressed()"), control.convert_to_grayscale)
        self.connect(self.normal_radio_button, SIGNAL("pressed()"), control.normal_colours)
        self.connect(self.sepia_radio_button, SIGNAL("pressed()"), control.convert_to_sepia)

        self.connect(self.dial, SIGNAL("valueChanged(int)"), self.dial_change) #calls a predifined method in spinbox and in dial
        self.connect(self.spinbox, SIGNAL("valueChanged(int)"), self.spinbox_change) #vienas kit? kei?ia(pa?i?r?ti paleidus)
        self.connect(self.checkbox, SIGNAL("clicked()"), self.gaussian_blur_enable)

        self.connect(self.watermark_checkbox, SIGNAL("clicked()"), self.watermark_changed)

    def watermark_changed(self):
        if self.watermark_checkbox.isChecked():
            control.enable_watermark()
            return
        else:
            control.disable_watermark()

    def gaussian_blur_enable(self):
        if self.checkbox.isChecked():
            control.enable_gaussian_blur()
            return
        else:
            control.disable_gaussian_blur()

    def dial_change(self, int): #int gauna i? SIGNAL
        self.checkbox.setChecked(True)
        self.gaussian_blur_enable()
        self.spinbox.setValue(int)
        control.set_gaussian_blur(int)
        

    def spinbox_change(self, int):
        self.dial.setValue(int)
        control.set_gaussian_blur(int)

    def start_stop_pressed(self):
        if self.start_stop_button.text() == "Start":
            self.start_stop_button.setText("Cancel")
            control.start()
        else:
            self.start_stop_button.setText("Start")
            control.stop()


class QFrameEfekto3(QFrame):
    def __init__(self, parent = None):
        super(QFrameEfekto3, self).__init__(parent)
        self.name = 'Effect3'
        self.runs = False

        control.set_effect_to_control(self.name)
        #Buttons
        self.start_stop_button = QPushButton(text = "Start")
        self.saugoti_button = QPushButton(text = "Save")
        
        #Tekstas
        self.negalima_saugoti = QLabel()
        #saugojimo layout
        saugojimo_layout = QVBoxLayout()
        saugojimo_layout.addWidget(self.saugoti_button)
        saugojimo_layout.addWidget(self.negalima_saugoti)
        saugojimas = QGroupBox(u'Save Image')
        saugojimas.setLayout(saugojimo_layout)
        #Dropbox
        self.dropbox = QComboBox()
        self.populate_dropbox()
        dropbox_layout = QHBoxLayout()
        dropbox_layout.addWidget(self.dropbox)
        paveikslelis = QGroupBox('Select Image')
        paveikslelis.setLayout(dropbox_layout)
        #Grid
        grid = QGridLayout()

        grid.addWidget(paveikslelis, 1, 0)
        grid.addWidget(saugojimas, 2, 0)
        grid.addWidget(self.start_stop_button, 3, 0)

        self.setLayout(grid)

        self.connect(self.start_stop_button, SIGNAL("clicked()"), self.start_stop_pressed)

        self.dropbox.currentIndexChanged.connect(self.dropbox_changed)

        self.connect(self.saugoti_button, SIGNAL("clicked()"), self.saugoti)

    def saugoti(self):
        if not self.runs:
            self.negalima_saugoti.setText('First start the program')
            return
        fil_dir = QFileDialog.getSaveFileName(self, 'Save file', '', '.jpg')
        if fil_dir[0] == '':
            return
        control.issaugoti_paveiksleli(fil_dir)


    def dropbox_changed(self, index):
        control.keisti_paveiksleli(self.dropbox.itemText(index))

    def populate_dropbox(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '\\img' #gets file directory
        img_list = get_imlist(path, 'png')
        for n, img in enumerate(img_list):
            name = img[img.rfind('\\') + 1:-4]
            self.dropbox.insertItem(n, name, img)


    def start_stop_pressed(self):
        if self.start_stop_button.text() == "Start":
            self.negalima_saugoti.setText('')
            self.start_stop_button.setText("Cancel")
            self.runs = True
            control.start()
        else:
            self.start_stop_button.setText("Start")
            self.runs = False
            control.stop()



class Tabs(QTabWidget):
    def __init__(self, parent = None):
        super(Tabs, self).__init__(parent)        

        tab1 = QFrameEfekto1()
        tab2 = QFrameEfekto2()
        tab3 = QFrameEfekto3()

        self.addTab(tab2, "Effect1")
        self.addTab(tab3, "Effect2")

        self.currentChanged.connect(self.tabswitch)

    def tabswitch(self):
        self.currentWidget().start_stop_button.setText("Start") #nustato text button ? 'start' pakeitus tab
        control.stop()
        control.set_effect_to_control(self.currentWidget().name)


app = QApplication(sys.argv) #Create a Qt application
control = controller.Control() #creates controler

gui = Tabs()
gui.show()
app.exec_() #enter the Qt main loop and start to execute the Qt code