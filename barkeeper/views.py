import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
sys.modules['Picamera'] = fake_rpi.picamera # Fake picamera
print(sys.modules['RPi.GPIO'])
from django.contrib.auth.models import User
from rest_framework import permissions
from barkeeper.models import Event
from barkeeper.utils import *
from barkeeper.serializers import EventSerializer, UserSerializer
from rest_framework import generics
from django.shortcuts import redirect, render

import RPi.GPIO as GPIO
import Picamera

Pins = {
   13: {"name" : "gripper", "homing_pos": 60, "sleep_time":0.2,"task_pos":0, "sleep_time_task":0.05},
   11: {"name" : "wrist", "homing_pos": 0, "sleep_time":0.0,"task_pos":80, "sleep_time_task":0.0},
   15: {"name" : "upper_arm", "homing_pos": 150, "sleep_time":0.0,"task_pos":120, "sleep_time_task":0.0},
   37: {"name" : "lower_arm", "homing_pos": 120, "sleep_time":0.0,"task_pos":0, "sleep_time_task":0.0},
   35: {"name" : "waist", "homing_pos": 0, "sleep_time":0.0,"task_pos":0, "sleep_time_task":0.0}
}

def index(request):
    active_1 = 1
    active_2 = 1
    active_3 = 1
    active_4 = 1
    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4})

def robot_homing(request):
    active_1 = 1
    active_2 = 1
    active_3 = 1
    active_4 = 1
    for pin,config in Pins.items():
        GPIO.setmode(GPIO.BOARD)
        motor = motor_setup(pin)
        homing_pos = config["homing_pos"]
        dc = degree_to_DC(homing_pos)
        change_DC(motor,dc)
        time.sleep(config["sleep_time"])
        clean_up(motor)
    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4})

def robot_grab(request):
    active_1 = 1
    active_2 = 1
    active_3 = 1
    active_4 = 1
    GPIO.setmode(GPIO.BOARD)
    gripper = motor_setup(13)
    wrist = motor_setup(11)
    test_range(gripper)
    clean_up(gripper)
    test_range(wrist)
    clean_up(wrist)
    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4})

def camera_start(request):
    active_1 = 1
    camera = Picamera()
    camera.framerate = 30
    camera.preview_fullscreen=False
    camera.preview_window=(640, 480, 640, 480)
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()
    camera_switch = False
    return render(request,"index.html",{'active_1':active_1})

def loadcell_start(request):
    active_2 = 1
    return render(request,"index.html",{'active_2':active_2})

def robot_homing(request):
    active_3 = 1
    return render(request,"index.html",{'active_3':active_3})

def event_create(request):
    active_1 = 1
    active_2 = 1
    active_3 = 1
    active_4 = 1
    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4})


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BarkeepingHistory(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def get(self, request, format=None):
    #     events = Event.objects.all()
    #     serializer = EventSerializer(events, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = EventSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BarkeepingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 
    
    # def get_object(self, pk):
    #     try:
    #         return Event.objects.get(pk=pk)
    #     except Event.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     event = self.get_object(pk)
    #     serializer = EventSerializer(event)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     event = self.get_object(pk)
    #     serializer = EventSerializer(event, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     event = self.get_object(pk)
    #     event.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

