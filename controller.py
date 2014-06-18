from Efektai import *
from utilities import *

class Control:
    def __init__(self):
        self.efektas = None
    
    def set_effect_to_control(self, efektas):
        komanda = 'self.efektas =' + efektas + '()'
        exec (komanda)

    def start(self):
        self.efektas.start()

    def stop(self):
        if self.efektas:
            self.efektas.stop()

    def convert_to_grayscale(self):
        self.efektas.grayscale = True
        self.efektas.sepia = False

    def normal_colours(self):
        self.efektas.grayscale = False
        self.efektas.sepia = False

    def convert_to_sepia(self):
        self.efektas.grayscale = False
        self.efektas.sepia = True

    def set_gaussian_blur(self, blur_str):
        self.efektas.blur_strength = blur_str

    def enable_gaussian_blur(self):
        self.efektas.gaussian_blur_state = True

    def disable_gaussian_blur(self):
        self.efektas.gaussian_blur_state = False

    def enable_watermark(self):
        self.efektas.watermark = True

    def disable_watermark(self):
        self.efektas.watermark = False

    def keisti_paveiksleli(self, name):
        self.efektas.image_read(name)

    def issaugoti_paveiksleli(self, save_to):
        self.efektas.save = True
        self.efektas.save_dir = save_to