from django.contrib.auth.models import User
from barkeeper.models import Event
from rest_framework import serializers
from rest_framework import permissions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def create_event(self, validated_data):
        return Event.objects.create(**validated_data)

    def update_event(self, instance, validated_data):
        instance.picamera_img_val = validated_data.get('picamera_img_val', instance.picamera_img_val)
        instance.ocr_text = validated_data.get('ocr_text', instance.ocr_text)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.score = validated_data.get('score', instance.score)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance