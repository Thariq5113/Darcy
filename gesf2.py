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


def rightnormal_servos():
    kit.servo[SR].angle = 0
    kit.servo[UR].angle = 0
    kit.servo[ER].angle = 90
    kit.servo[FR].angle = 0
    print("Servos set to normal position")
    time.sleep(0.5)

def leftnormal_servos():
    kit.servo[SL].angle = 180
    kit.servo[UL].angle = 180
    kit.servo[EL].angle = 90
    kit.servo[FL].angle = 180
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
        #kit.servo[SL].angle = 
        kit.servo[UL].angle = 100
        time.sleep(0.5)
        kit.servo[EL].angle = 15
        time.sleep(0.5)
        kit.servo[FL].angle = 90
        time.sleep(0.5)
        kit.servo[FL].angle = 180
        time.sleep(0.5)
        kit.servo[FL].angle = 90
        time.sleep(0.5)
        kit.servo[FL].angle = 180
        time.sleep(0.5)
        kit.servo[FL].angle = 90
        time.sleep(0.5)
        kit.servo[FL].angle = 180
        time.sleep(0.5)
        
    leftnormal_servos()

def salute_action():
    print("Performing Salute")
    kit.servo[SR].angle = 140
    kit.servo[UR].angle = 90
    kit.servo[ER].angle = 45
    time.sleep(1)
    normal_servos()

def clap_action():
    print("Clapping Hands")

    # Step 1: Move shoulders and upper arms inward
    for angle in range(180, 100, -5):  # move inward
        kit.servo[SR].angle = angle
        kit.servo[SL].angle = angle
        kit.servo[UR].angle = angle
        kit.servo[UL].angle = angle
        time.sleep(0.02)

    # Step 2: Bend elbows to bring hands closer
    for angle in range(90, 60, -5):  # bend elbow inward
        kit.servo[ER].angle = angle
        kit.servo[EL].angle = angle
        time.sleep(0.02)

    # Step 3: Simulate clapping motion (move wrists)
    for i in range(3):  # Clap 3 times
        kit.servo[FR].angle = 60  # clap in
        kit.servo[FL].angle = 60
        time.sleep(0.25)
        kit.servo[FR].angle = 90  # clap out
        kit.servo[FL].angle = 90
        time.sleep(0.25)

    # Step 4: Reset all to neutral
    normal_servos()
    
def handshake_action():
    print("Shaking Hand")

    # Step 1: Extend shoulder and upper arm forward
    for angle in range(180, 100, -5):  # shoulder + upper arm forward
        kit.servo[SR].angle = angle
        kit.servo[UR].angle = angle
        time.sleep(0.02)

    # Step 2: Bend elbow to bring hand out
    for angle in range(90, 60, -5):  # elbow bends
        kit.servo[ER].angle = angle
        time.sleep(0.02)

    # Step 3: Shake forearm (up and down motion)
    for i in range(3):  # Shake 3 times
        kit.servo[FR].angle = 80  # down
        time.sleep(0.2)
        kit.servo[FR].angle = 100  # up
        time.sleep(0.2)

    # Step 4: Return to normal position
    normal_servos()


if __name__ == "__main__":

   #namaste_action()
    wave_action()
