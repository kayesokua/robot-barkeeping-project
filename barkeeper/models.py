from django.db import models
from datetime import datetime

# Create your models here.
class Event(models.Model):
    picamera_img_val = models.TextField()
    ocr_text = models.TextField(default="default")
    weight = models.DecimalField(max_digits=19, decimal_places=10)
    score = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.ocr_text