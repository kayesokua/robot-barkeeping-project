from django.test import TestCase
from RPi import GPIO

Pins = {
   13: {"name" : "gripper", "homing_pos": 60, "sleep_time":0.2,"task_pos":0, "sleep_time_task":0.05},
   11: {"name" : "wrist", "homing_pos": 0, "sleep_time":0.0,"task_pos":80, "sleep_time_task":0.0},
   15: {"name" : "upper_arm", "homing_pos": 150, "sleep_time":0.0,"task_pos":120, "sleep_time_task":0.0},
   37: {"name" : "lower_arm", "homing_pos": 120, "sleep_time":0.0,"task_pos":0, "sleep_time_task":0.0},
   35: {"name" : "waist", "homing_pos": 0, "sleep_time":0.0,"task_pos":0, "sleep_time_task":0.0}
}

class MotorGPIOTests(TestCase):
    def setup_motor_gripper(self):
        gripper_pin = 13
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gripper_pin, GPIO.OUT)
        self.assertEqual(GPIO.getmode(), GPIO.BOARD)
        self.assertEqual(gripper_pin, 13)

    def setup_motor_wrist(self):
        wrist_pin = 11
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(wrist_pin, GPIO.OUT)
        self.assertEqual(GPIO.getmode(), GPIO.BOARD)
        self.assertEqual(wrist_pin, 11)

    def setup_motor_upper_arm(self):
        upper_arm_pin = Pins[15]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(upper_arm_pin, GPIO.OUT)
        self.assertEqual(GPIO.getmode(), GPIO.BOARD)
        self.assertEqual(upper_arm_pin, 15)

    def setup_motor_lower_arm(self):
        lower_arm_pin = 37
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(lower_arm_pin, GPIO.OUT)
        self.assertEqual(GPIO.getmode(), GPIO.BOARD)
        self.assertEqual(lower_arm_pin, 37)

    def setup_motor_waist(self):
        waist_pin = 35
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(waist_pin, GPIO.OUT)
        self.assertEqual(GPIO.getmode(), GPIO.BOARD)
        self.assertEqual(waist_pin, 35)

    def test_pwm(self):
        pin = 13
        pwm = GPIO.PWM(pin, 50)
        pwm.start(0)
        pwm.ChangeDutyCycle(1)
        pwm.ChangeDutyCycle(2)
        pwm.stop()
        GPIO.cleanup(pin)

    def test_mode(self):
        GPIO.setmode(GPIO.BCM)
        self.assertEqual(11, GPIO.BCM)
        GPIO.setmode(GPIO.BOARD)
        self.assertEqual(10, GPIO.BOARD)

    def test_gpio_function(self):
        GPIO.setmode(GPIO.BCM)
        try:
            for i in range(54):
                GPIO.gpio_function(i)
        except:
            self.fail("GPIO.gpio_function raised an inexpected error!")

    def test_cleanup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(0, GPIO.OUT)
        GPIO.cleanup()
        self.assertEqual(1, GPIO.IN)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([0], GPIO.OUT)
        GPIO.cleanup([0])
        self.assertEqual(1, GPIO.IN)