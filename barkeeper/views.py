from difflib import diff_bytes
import random
import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
sys.modules['Picamera'] = fake_rpi.picamera # Fake picamera
print(sys.modules['RPi.GPIO'])
from django.contrib.auth.models import User
from rest_framework import permissions
from barkeeper.models import Event
from barkeeper.forms import EventForm
from barkeeper.utils import *
from barkeeper.serializers import EventSerializer, UserSerializer
from rest_framework import generics
from django.shortcuts import redirect, render, get_object_or_404
from random_word import RandomWords

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
    imarray = np.random.rand(480,640,3) * 255
    mock_imarray = str(imarray)
    randomized_array = mock_imarray[:1000]
    r = RandomWords()
    randomized_text = r.get_random_word()
    randomized_weight = random.randint(40, 61)
    randomized_score = random.choice([False,False])

    if request.method == 'GET':
        return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4,
            "form_event_dummy":EventForm(),
            "randomized_text":randomized_text,
            "randomized_array":randomized_array,
            "randomized_weight":randomized_weight,
            "randomized_score":randomized_score  
        })    
    else:
        if request.method == 'POST':
            dummy_form = EventForm(request.POST)
            if dummy_form.is_valid():
                 dummy_form.save()
                 return redirect('event_history')
            else:
                return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4,
            "form_event_dummy":EventForm(),
            "randomized_text":randomized_text,
            "randomized_array":randomized_array,
            "randomized_weight":randomized_weight,
            "randomized_score":randomized_score,
            "result":"something went wrong!"
        })

def event_read(request, pk):
    e = get_object_or_404(Event, pk=pk)
    return render(request,"read.html",{"e":e})

def event_update(request, pk):
    e = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('event_history')
    else:
        return redirect('event_update')

def event_delete(request, pk):
    e = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        e.delete()
        return redirect('events_history')


def robot_homing(request):
    active_1 = 0
    active_2 = 0
    active_3 = 1
    active_4 = 0

    for pin,config in Pins.items():
        GPIO.setmode(GPIO.BOARD)
        motor = motor_setup(pin)
        homing_pos = config["homing_pos"]
        dc = degree_to_DC(homing_pos)
        change_DC(motor,dc)
        time.sleep(config["sleep_time"])
        clean_up(motor)
    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4, "result": "Homing has successfully completed."})

def robot_grab(request):
    active_1 = 0
    active_2 = 0
    active_3 = 1
    active_4 = 0
    GPIO.setmode(GPIO.BOARD)
    gripper = motor_setup(13)
    wrist = motor_setup(11)
    test_range(gripper)
    clean_up(gripper)
    test_range(wrist)
    clean_up(wrist)
    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4, "result": "Grab has successfully completed."})

def robot_pour(request):
    active_1 = 0
    active_2 = 0
    active_3 = 1
    active_4 = 0
    GPIO.setmode(GPIO.BOARD)
    gripper = motor_setup(13)
    wrist = motor_setup(11)
    test_range(gripper)
    clean_up(gripper)
    test_range(wrist)
    clean_up(wrist)
    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4, "result": "Pouring has successfully completed."})


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
    # ocr_text
    return render(request,"index.html",{'active_1':active_1})

# Functions for Load Cell starts here

def hx711_setup():
    GPIO.setwarnings(False)
    # Calculating the reference unit
    # If I got numbers around 32873 for an empty shot glass that weights 80g
    # Then reference unit is 32873 / 80 = 410.91
    referenceUnit = 32873/80
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)

def loadcell_start(request):
    active_1 = 0
    active_2 = 1
    active_3 = 0
    active_4 = 0

    referenceUnit = 32873/80
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx711_setup()
    hx.reset()
    hx.tare()
    hx.tare_A()
    hx.tare_B()
    print("Let us begin weighing..")
    
    for i in range(0,20):
        val = hx.get_weight(5)
        res = "{:.2f}".format(val)
        print("Weigh sensor reads ",res, "g")
        hx.power_down()
        hx.power_up()
        time.sleep(1)

        if int(val) > 60 and int(val) < 120:
            print("We recognise an empty shot glass!")
            print("Now its time to wait for the robot!")
            time.sleep(3)
            clean_up()
            print(val)
            return render(request,"index.html", {"result":"It's an empty cup!",'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4})
        else:
            return render(request,"index.html", {"result":"It doesn't look like an empty cup!",'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4})

def robot_kinematics_forward(request):
    return render(request,"kinematics_forward.html")

def robot_kinematics_forward_result(request):
    theta_1 =float(request.GET['angle_1'])
    theta_2 =float(request.GET['angle_2'])
    theta_3 =float(request.GET['angle_3'])
    theta_4 =float(request.GET['angle_4'])
    
    answer = forward_kinematics(theta_1,theta_2,theta_3,theta_4)
    
    return render(request,"kinematics_forward.html",
    {'theta_1':theta_1,
    'theta_2':theta_2,
    'theta_3':theta_3,
    'theta_4':theta_4,
    'answer':answer})

def robot_kinematics_inverse(request):
    return render(request,"kinematics_inverse.html")

def robot_kinematics_inverse_result(request):
    displacement_x =float(request.GET['target_x'])
    displacement_y =float(request.GET['target_y'])
    displacement_z =float(request.GET['target_z'])
    answer = inverse_kinematics(displacement_x,displacement_y,displacement_z)
    return render(request,"kinematics_inverse.html",
    {'d_x':displacement_x,
    'd_y':displacement_y,
    'd_z':displacement_z,
    'answer':answer})

def event_create(request):
    active_1 = 1
    active_2 = 1
    active_3 = 1
    active_4 = 1
    # start camera
        # if ocr_text found in dictionary:
            # start load cell
                # if load cell success:
                    # robot homing
                    # robot grabs a bottle from position 1
                    # robot start to pour
                    # robot grabs a bottle from position 2
                    # robot start to pour
                    # start load cell and get resulting weight
                        # if load cell confirms the weight has changed
                        # confirm with customer: was it successful?
                        # the events end
            # else: ask customer to start all over

    return render(request,"index.html", {'active_1':active_1,'active_2':active_2,'active_3':active_3,'active_4':active_4})

#def event_view(request):
#    queryset = Post.objects.filter(status=1).order_by("-created_on")

def event_history(request):
    successful_drinks = Event.objects.filter(score=True).order_by("-created_at")
    failed_drinks = Event.objects.filter(score=False).order_by("-created_at")
    return render(request,"events.html", {'successful_drinks':successful_drinks,'failed_drinks':failed_drinks})

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

