from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from django.contrib.auth.models import User
from barkeeper.models import Event
from django.test import TestCase
from barkeeper.models import Event
from django.utils import timezone
from django.urls import reverse
from random_word import RandomWords
from unittest import mock
import numpy
import yaml
import pytz
import datetime
import random
import decimal

imarray = numpy.random.rand(480,640,3) * 255
mock_imarray = str(imarray)
cut_mock_imarray = mock_imarray[:1000]

r = RandomWords()
mock_text = r.get_random_word()
mock_weight = round(random.uniform(40, 80),2)
mock_score = random.choice([True, False])
mock_date = datetime.datetime(2022, 5, 13, 4, 0, 2, tzinfo=pytz.utc)

MODELS = [Event,]

class EventTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user('supercoder', 'supercoder@rbk.com', '123abc')
        self.test_user.is_superuser = True
        self.test_user.is_active = True
        self.test_user.save()
        self.assertEqual(self.test_user.is_superuser, True)
        login = self.client.login(username='supercoder', password='123abc')
        self.failUnless(login, 'Could not log in')
    
    def tearDown(self):
        for model in MODELS:
            for obj in model.objects.all():
                obj.delete()
                
    def test_create_event(self):
        new_event = Event.objects.create(
            picamera_img_val=cut_mock_imarray,
            ocr_text=mock_text,
            weight=mock_weight,
            score=mock_score,
            created_at=mock_date
        )
        new_event.save()
        
    def test_event_model(self):
        e = Event.objects.first()
        
        self.assertEqual(cut_mock_imarray, e.picamera_img_val)
        self.assertEqual(mock_text, e.ocr_text)
        self.assertEqual(mock_weight, e.weight)
        self.assertEqual(mock_score, e.score)
        self.assertEqual(mock_date, e.created_at)
