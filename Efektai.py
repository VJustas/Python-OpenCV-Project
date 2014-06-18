#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import cv2
import numpy

from cv2 import cv

#veido atpazinimui reikalingi kintamieji ir vieta jiems saugoti
storage = cv.CreateMemStorage()
haarFace = cv.Load('haarcascade_frontalface_default.xml')
haarEyes = cv.Load('haarcascade_eye.xml')

class Effect1:
    def efektas(self, frame):
        return frame

    def start(self):
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(3, 960) #nustato vaizdo kameros dydį
        self.webcam.set(4, 720)
        while True:
            _,frame = self.webcam.read() #frame nuskaityms i? stream _ - naudojamas, kad igoruotu pirm? argument? gra?inama i? tuple
            frame = self.efektas(frame)
            cv2.imshow('Video', frame)
            
            k = cv2.waitKey(20) 
            if k == 27:
                break

    def stop(self):
        cv2.destroyAllWindows()
        self.webcam.release()

class Effect2(Effect1):
    def __init__(self): 
        self.grayscale = False #pradinei parametrai
        self.sepia = False
        self.blur_strength = 0
        self.watermark = True
        self.gaussian_blur_state = False

    def efektas(self, frame):
        frame = self.gaussian_blur(frame) #kadras apdorojamas su gaussian blur
        frame = self.watermarking(frame) #uzdeda watermark
        if self.grayscale:  #pilkas filtras
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
        if self.sepia: #sepia filtras
            frame = self.convert_to_sepia(frame)
        return frame

    def watermarking(self, frame):
        """Vandens zymes dejimas"""
        if self.watermark:
            s_img = cv2.imread('img/20090715121700!Vdu_logo.png', -1)
            s_img = cv2.resize(s_img, (64, 64))
            x_offset=y_offset=10
            for c in range(0,3):
                frame[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] = s_img[:,:,c] * (s_img[:,:,3]/255.0) +  frame[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] * (1.0 - s_img[:,:,3]/255.0)
        return frame

    def convert_to_sepia(self, frame):
        """Sepia filtras"""
        m_sepia = numpy.asarray([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
        sepia = cv2.transform(frame, m_sepia)
        sepia = cv2.cvtColor(sepia, cv2.cv.CV_RGB2BGR)
        return sepia

    def gaussian_blur(self, frame): #blur_strength gal nevisai atitinka tai ka isites daro funkcija
        if self.blur_strength != 0 and self.gaussian_blur_state:
            frame = cv2.GaussianBlur(frame, (0,0), self.blur_strength)
        return frame


class Effect3(Effect1):
    def __init__(self):
        self.image = cv2.imread('img/akiniai.png', -1) #paveikslelis padengti veidui
        self.save = False #pradinei parametrai
        self.save_dir = None

    def efektas(self, frame):
        """taikomu efektu eilė"""
        frame = self.pav_dejimas_ant_veido(frame)
        if self.save:
            self.save_picture(frame, self.save_dir)
            self.save = False
        return frame

    def veido_atpazinimas(self, frame):
        """Veido atpazinimo metodas"""
        frame = cv.fromarray(frame)
        # running the classifiers        
        detectedFace = cv.HaarDetectObjects(frame, haarFace, storage)

        if detectedFace:            
            for face in detectedFace:
                cv.Rectangle(frame,(face[0][0],face[0][1]),
                            (face[0][0]+face[0][2],face[0][1]+face[0][3]),
                            cv.RGB(155, 255, 25),2)

        frame = numpy.asarray(frame)
        return frame

    def image_read(self, name):
        """Paveikslelio nuskaitymas"""
        self.image = cv2.imread('img/' + name +'.png', -1)

    def pav_dejimas_ant_veido(self, frame):
        """Paveikslelio dejimas ant veido"""
        frame_cvmat = cv.fromarray(frame) #sukuriamas kadras kitu formatu
        webcam_width = self.webcam.get(3) #cameros resoliuzijos gavimas
        webcam_height = self.webcam.get(4)

        # running the classifiers        
        detectedFace = cv.HaarDetectObjects(frame_cvmat, haarFace, storage)

        #rasta veida dengia paveiksleliu
        if detectedFace:
            for face in detectedFace:                
                s_img = self.image
                s_img = cv2.resize(s_img, (face[0][2], face[0][3]))               
                if face[0][2] > webcam_width - face[0][0] and face[0][3] > webcam_height - face[0][1]:
                    s_img = s_img[0:webcam_width - face[0][0], 0:webcam_height - face[0][1]]
                    print s_img.shape[0], s_img.shape[1]
                x_offset=face[0][0]
                y_offset=face[0][1]
                for c in range(0,3):                    
                    frame[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] = s_img[:,:,c] * (s_img[:,:,3]/255.0) +  frame[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1], c] * (1.0 - s_img[:,:,3]/255.0)
        return frame

    def save_picture(self, frame, dir):
        cv2.imwrite(dir[0], frame)
