import sys
import fake_rpi
sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['picamera'] = fake_rpi.picamera # Fake picamera
from fake_rpi.wrappers import printf
from fake_rpi.Base import Base

import numpy as np
from django.test import TestCase
from picamera import PiCamera
#from picamera.array import PiRGBArray

import datetime
from time import sleep
import requests
from PIL import Image
from numpy import asarray
#import pytesseract

class CameraTest(TestCase):
    def setUp(self):
        camera = PiCamera()
        camera.framerate = 30
        camera.preview_fullscreen=False
        camera.preview_window=(640, 480, 640, 480)
        camera.resolution = (640, 480)
        self.assertEqual(camera.framerate,30)
        self.assertEqual(camera.preview_fullscreen,False)
        self.assertEqual(camera.preview_window,(640, 480, 640, 480))
        self.assertEqual(camera.resolution,(640, 480))