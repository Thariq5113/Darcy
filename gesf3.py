from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

# Servo mapping
SR = 0
UR = 1
ER = 2
FR = 3
SL = 12
UL = 13
EL = 14
FL = 15
WR= 4

def normal_servos():
    kit.servo[SR].angle = 0
    kit.servo[UR].angle = 0
    kit.servo[ER].angle = 90
    kit.servo[FR].angle = 0
    print("Servos set to normal position")
    time.sleep(0.5)



def namaste_action():
    print("Performing Namaste")
    for angle in range(180, 90, -5):
        kit.servo[SR].angle = angle
        kit.servo[SL].angle = angle
        time.sleep(0.05)
    for angle in range(180, 90, -5):
        kit.servo[UR].angle = angle
        kit.servo[UL].angle = angle
        time.sleep(0.05)
    for angle in range(90, 45, -5):
        kit.servo[ER].angle = angle
        kit.servo[EL].angle = angle
        time.sleep(0.05)
    time.sleep(1)
    normal_servos()

def wave_action():
    print("Waving Hand")
    
    for i in range(1):
        kit.servo[SR].angle = 0
        kit.servo[UR].angle = 65
        time.sleep(0.5)
        kit.servo[ER].angle = 180
        time.sleep(0.5)
        kit.servo[FR].angle = 90
        time.sleep(0.5)
        kit.servo[FR].angle = 0
        time.sleep(0.5)
        kit.servo[FR].angle = 90
        time.sleep(0.5)
        kit.servo[FR].angle = 0
        time.sleep(0.5)
        kit.servo[FR].angle = 90
        time.sleep(0.5)
        kit.servo[FR].angle = 0
        time.sleep(0.5)
        
    normal_servos()

def salute_action():
    print("Performing Salute")
    kit.servo[SR].angle = 140
    kit.servo[UR].angle = 90
    kit.servo[ER].angle = 45
    time.sleep(1)
    normal_servos()

def hello_action():
    print("Performing Hello Gesture")

    # Step 1: Move SR and FR to starting gesture positions
    kit.servo[SR].angle = 45
    kit.servo[FR].angle = 90
    time.sleep(1)

    # Step 2: Finger up/down shake (around 90°)
    for i in range(2):
        kit.servo[FR].angle = 75  # Move down
        time.sleep(0.5)
        kit.servo[FR].angle = 105  # Move up
        time.sleep(0.5)

    # Step 3: Return FR to base (90°) before reset
    kit.servo[FR].angle = 90
    time.sleep(1)

    # Step 4: Sudden reset to initial positions
    kit.servo[SR].angle = 0
    time.sleep(0.5)
    kit.servo[FR].angle = 0
    time.sleep(0.5)
    print("Hello Gesture Complete")
    
# Channel for grabbing servo (use any free channel, e.g., 4)


def grab_action():
    print("Grabbing...")
    kit.servo[WR].set_pulse_width_range(500, 2500)  # MG995 typical range
    kit.servo[WR].angle = 180
    time.sleep(1)

def release_action():
    print("Releasing...")
    kit.servo[WR].angle = 0
    time.sleep(1)

def clap_action():
    print("Clapping Hands")
    for angle in range(180, 90, -5):
        kit.servo[SR].angle = angle
        kit.servo[SL].angle = angle
        time.sleep(0.02)
    for angle in range(90, 60, -5):
        kit.servo[ER].angle = angle
        kit.servo[EL].angle = angle
        time.sleep(0.02)
    for i in range(2):
        kit.servo[ER].angle = 60
        kit.servo[EL].angle = 60
        time.sleep(0.3)
        kit.servo[ER].angle = 90
        kit.servo[EL].angle = 90
        time.sleep(0.3)
    normal_servos()

if __name__ == "__main__":

   #namaste_action()
    wave_action()

