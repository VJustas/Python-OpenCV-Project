import sys

from PySide.QtGui import *
from PySide.QtCore import *

import cv2
import numpy as np

class Form(QTabWidget):

    c = cv2.VideoCapture(0)

    def __init__(self, parent = None):
        super(Form, self).__init__(parent)

        self.start_stop_button = QPushButton(text = "Start")
        dial = QDial()
        dial.setNotchesVisible(True)

        tab1 = QFrame()
        grid = QGridLayout()
        grid.addWidget(dial, 0, 0)
        grid.addWidget(self.start_stop_button, 1, 0)
        tab1.setLayout(grid)
        self.addTab(tab1, "Efektas1")

        tab2 = QFrame()
        grid2 = QGridLayout()       
        tab2.setLayout(grid2)
        self.addTab(tab2, "Efektas2")

        tab3 = QFrame()
        grid3 = QGridLayout()       
        tab3.setLayout(grid3)
        self.addTab(tab3, "Efektas3")

        self.connect(self.start_stop_button, SIGNAL("clicked()"), self.start_stop_pressed)


    def start_stop_pressed(self):
        if self.start_stop_button.text() == "Start":
            self.start_stop_button.setText("Cancel")
            self.start()
        else:
            self.start_stop_button.setText("Start")
            self.kill()

    def start(self):
        _,f = self.c.read()
 
        avg1 = np.float32(f)
        avg2 = np.float32(f)
        while(1):
            _,f = self.c.read()
     
            cv2.accumulateWeighted(f,avg1,0.1)
            cv2.accumulateWeighted(f,avg2,0.01)
     
            res1 = cv2.convertScaleAbs(avg1)
            res2 = cv2.convertScaleAbs(avg2)
 
            cv2.imshow('img',f)
            cv2.imshow('avg1',res1)
            cv2.imshow('avg2',res2)
            k = cv2.waitKey(20)
 
            if k == 27:
                break

    def kill(self):
        cv2.destroyAllWindows()
        self.c.release()


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()