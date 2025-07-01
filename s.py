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
WR = 4

# Default speed factors for all 9 servos (1.0 = normal speed)
DEFAULT_SPEED_FACTORS = {
    'SL': 1.0, 'UL': 1.0, 'EL': 1.0, 'FL': 1.0,
    'SR': 1.0, 'UR': 1.0, 'ER': 1.0, 'FR': 1.0,
    'WR': 1.0
}

def leftnormal_servos(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Setting Left Servos to Attention Position")
    
    sl_speed = speed_factors.get('SL')
    ul_speed = speed_factors.get('UL')
    el_speed = speed_factors.get('EL')
    fl_speed = speed_factors.get('FL')
    
    base_delay_sl = 0.05 * sl_speed
    step_size_sl = max(1, int(5 / sl_speed))
    base_delay_ul = 0.05 * ul_speed
    step_size_ul = max(1, int(5 / ul_speed))
    base_delay_el = 0.05 * el_speed
    step_size_el = max(1, int(5 / el_speed))
    base_delay_fl = 0.05 * fl_speed
    step_size_fl = max(1, int(5 / fl_speed))
    
    current_sl = kit.servo[SL].angle if kit.servo[SL].angle is not None else 0
    current_ul = kit.servo[UL].angle if kit.servo[UL].angle is not None else 0
    current_el = kit.servo[EL].angle if kit.servo[EL].angle is not None else 0
    current_fl = kit.servo[FL].angle if kit.servo[FL].angle is not None else 0
    
    print(f"SL: Moving to 180, base_delay={base_delay_sl:.3f}s, step_size={step_size_sl}deg")
    for angle in range(int(current_sl), 180, step_size_sl if current_sl < 180 else -step_size_sl):
        kit.servo[SL].angle = angle
        time.sleep(base_delay_sl)
    
    print(f"UL: Moving to 180, base_delay={base_delay_ul:.3f}s, step_size={step_size_ul}deg")
    for angle in range(int(current_ul), 180, step_size_ul if current_ul < 180 else -step_size_ul):
        kit.servo[UL].angle = angle
        time.sleep(base_delay_ul)
    
    print(f"EL: Moving to 90, base_delay={base_delay_el:.3f}s, step_size={step_size_el}deg")
    for angle in range(int(current_el), 90, step_size_el if current_el < 90 else -step_size_el):
        kit.servo[EL].angle = angle
        time.sleep(base_delay_el)
    
    print(f"FL: Moving to 180, base_delay={base_delay_fl:.3f}s, step_size={step_size_fl}deg")
    for angle in range(int(current_fl), 180, step_size_fl if current_fl < 180 else -step_size_fl):
        kit.servo[FL].angle = angle
        time.sleep(base_delay_fl)
    
    time.sleep(0.5)
    print("Left servos set to attention position")

def rightnormal_servos(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Setting Right Servos to Attention Position")
    
    sr_speed = speed_factors.get('SR')
    ur_speed = speed_factors.get('UR')
    er_speed = speed_factors.get('ER')
    fr_speed = speed_factors.get('FR')
    
    base_delay_sr = 0.05 * sr_speed
    step_size_sr = max(1, int(5 / sr_speed))
    base_delay_ur = 0.05 * ur_speed
    step_size_ur = max(1, int(5 / ur_speed))
    base_delay_er = 0.05 * er_speed
    step_size_er = max(1, int(5 / er_speed))
    base_delay_fr = 0.05 * fr_speed
    step_size_fr = max(1, int(5 / fr_speed))
    
    current_sr = kit.servo[SR].angle if kit.servo[SR].angle is not None else 0
    current_ur = kit.servo[UR].angle if kit.servo[UR].angle is not None else 0
    current_er = kit.servo[ER].angle if kit.servo[ER].angle is not None else 0
    current_fr = kit.servo[FR].angle if kit.servo[FR].angle is not None else 0
    
    print(f"SR: Moving to 0, base_delay={base_delay_sr:.3f}s, step_size={step_size_sr}deg")
    for angle in range(int(current_sr), 0, step_size_sr if current_sr < 0 else -step_size_sr):
        kit.servo[SR].angle = angle
        time.sleep(base_delay_sr)
    
    print(f"UR: Moving to 0, base_delay={base_delay_ur:.3f}s, step_size={step_size_ur}deg")
    for angle in range(int(current_ur), 0, step_size_ur if current_ur < 0 else -step_size_ur):
        kit.servo[UR].angle = angle
        time.sleep(base_delay_ur)
    
    print(f"ER: Moving to 90, base_delay={base_delay_er:.3f}s, step_size={step_size_er}deg")
    for angle in range(int(current_er), 90, step_size_er if current_er < 90 else -step_size_er):
        kit.servo[ER].angle = angle
        time.sleep(base_delay_er)
    
    print(f"FR: Moving to 0, base_delay={base_delay_fr:.3f}s, step_size={step_size_fr}deg")
    for angle in range(int(current_fr), 0, step_size_fr if current_fr < 0 else -step_size_fr):
        kit.servo[FR].angle = angle
        time.sleep(base_delay_fr)
    
    time.sleep(0.5)
    print("Right servos set to attention position")

def grab_action(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Grabbing with left hand...")
    
    wr_speed = speed_factors.get('WR')
    base_delay = 0.05 * wr_speed
    step_size = max(1, int(5 / wr_speed))
    
    kit.servo[WR].set_pulse_width_range(500, 2500)  # MG995 typical range
    print(f"WR: Closing to 180, base_delay={base_delay:.3f}s, step_size={step_size}deg")
    for angle in range(0, 180, step_size):
        kit.servo[WR].angle = angle
        time.sleep(base_delay)
  
    
    
    

def release_action(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Grabbing with left hand...")
    
    wr_speed = speed_factors.get('WR')
    base_delay = 0.05 * wr_speed
    step_size = max(1, int(5 / wr_speed))
    
    kit.servo[WR].set_pulse_width_range(500, 2500)  # MG995 typical range

    print(f"WR: Opening to 0, base_delay={base_delay:.3f}s, step_size={step_size}deg")
    for angle in range(180, 0, -step_size):
        kit.servo[WR].angle = angle
        time.sleep(base_delay)
    
    #dssgf
    
def punch_action(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Performing Left Hand Shake")
    
    sr_speed = speed_factors.get('SR')
    ur_speed = speed_factors.get('UR')
    er_speed = speed_factors.get('ER')
    fr_speed = speed_factors.get('FR')
    
    base_delay_sr = 0.05 * sr_speed
    step_size_sr = max(1, int(5 / sr_speed))
    base_delay_ur = 0.05 * ur_speed
    step_size_ur = max(1, int(5 / ur_speed))
    base_delay_er= 0.05 * er_speed
    base_delay_fr= 0.05 * fr_speed
    grab_action()
    for angle in range(0, 90, step_size_sr): 
        kit.servo[FR].angle = angle
        time.sleep(base_delay_sr)
    for angle in range(0, 90, step_size_sr): 
        kit.servo[SR].angle = angle
        time.sleep(base_delay_sr) 
    for angle in range(90, 0, -step_size_sr): 
        kit.servo[FR].angle = angle
        time.sleep(base_delay_sr)
    
    time.sleep(base_delay_sr)
    rightnormal_servos(speed_factors={'SR': sr_speed, 'UR': ur_speed, 'ER': er_speed, 'FR': fr_speed})
    release_action()   
    #fdsfa
#poov
def rose_action(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Performing Left Hand Shake")
    
    sr_speed = speed_factors.get('SR')
    ur_speed = speed_factors.get('UR')
    er_speed = speed_factors.get('ER')
    fr_speed = speed_factors.get('FR')
    
    base_delay_sr = 0.05 * sr_speed
    step_size_sr = max(1, int(5 / sr_speed))
    base_delay_ur = 0.05 * ur_speed
    step_size_ur = max(1, int(5 / ur_speed))
    base_delay_er= 0.05 * er_speed
    base_delay_fr= 0.05 * fr_speed
    time.sleep(3)
    grab_action()
    for angle in range(0, 120, step_size_sr): 
        kit.servo[SR].angle = angle
        time.sleep(base_delay_sr)
    time.sleep(0.5)      
    release_action()   
    rightnormal_servos(speed_factors={'SR': sr_speed, 'UR': ur_speed, 'ER': er_speed, 'FR': fr_speed})
          

def shake_hand_action(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Performing Left Hand Shake")
    
    sr_speed = speed_factors.get('SR')
    ur_speed = speed_factors.get('UR')
    er_speed = speed_factors.get('ER')
    fr_speed = speed_factors.get('FR')
    
    base_delay_sr = 0.05 * sr_speed
    step_size_sr = max(1, int(5 / sr_speed))
    base_delay_ur = 0.05 * ur_speed
    step_size_ur = max(1, int(5 / ur_speed))
    base_delay_er= 0.05 * er_speed
    base_delay_fr= 0.05 * fr_speed
    
    for angle in range(0, 60, step_size_sr): 
        kit.servo[SR].angle = angle
        time.sleep(base_delay_sr)

    kit.servo[UR].angle = 0 # Upper arm stays right
    time.sleep(base_delay_ur)
    kit.servo[ER].angle = 90 # Elbow slightly right
    time.sleep(base_delay_er)

    time.sleep(2)
    for i in range(1):
        for angle in range(0, 60, step_size_sr):  
            kit.servo[FR].angle = angle  
            time.sleep(base_delay_ur)
        for angle in range(60, 0, -step_size_sr):  
            kit.servo[FR].angle = angle
            time.sleep(base_delay_ur)
    
    rightnormal_servos(speed_factors={'SR': sr_speed, 'UR': ur_speed, 'ER': er_speed, 'FR': fr_speed})
    print("Shake Hand Action Complete")




def salute_action(speed_factors=None):
    if speed_factors is None:
        speed_factors = {}
    speed_factors = {**DEFAULT_SPEED_FACTORS, **speed_factors}
    print("Performing Left Hand Salute")
    
    sl_speed = speed_factors.get('SL')
    ul_speed = speed_factors.get('UL')
    el_speed = speed_factors.get('EL')
    fl_speed = speed_factors.get('FL')
    
    base_delay_sl = 0.05 * sl_speed
    step_size_sl = max(1, int(5 / sl_speed))
    base_delay_ul = 0.05 * ul_speed
    base_delay_el = 0.05 * el_speed
    base_delay_fl = 0.05 * fl_speed
    
    for angle in range(180, 90, -step_size_sl): 
         # Gradual left move
        kit.servo[UL].angle = angle
        time.sleep(base_delay_ul)
    for angle in range(90, 0, -step_size_sl): 
        
        kit.servo[EL].angle = angle
        time.sleep(base_delay_el)
    for i in range(3):
        
        for angle in range(180, 90, -step_size_sl): 
            kit.servo[FL].angle = angle
            time.sleep(base_delay_el)
    
    
    leftnormal_servos(speed_factors)
    print("Salute Action Complete")

if __name__ == "__main__":
    print("Test 1: Slow UL Shake, Normal SL, EL, FL")
    rightnormal_servos()
    time.sleep(1)
    shake_hand_action(speed_factors={'UL': 10.0})
    time.sleep(1)
    
    print("\nTest 2: Fast UL Shake, Slow SL")
    rightnormal_servos(speed_factors={'SR': 0.5, 'UR': 0.5})
    time.sleep(1)
    shake_hand_action(speed_factors={'SL': 2.0, 'UL': 0.5})
    time.sleep(1)
    
    print("\nTest 3: Mixed Speeds for All Servos")
    rightnormal_servos(speed_factors={'SR': 2.0, 'UR': 1.0, 'ER': 0.5, 'FR': 1.0})
    time.sleep(1)
    shake_hand_action(speed_factors={'SL': 2.0, 'UL': 1.0, 'EL': 0.5, 'FL': 2.0})
    time.sleep(1)
    
    print("\nTest 4: Grab and Salute with Default Speeds")
    grab_action()
    time.sleep(1)
    salute_action()
