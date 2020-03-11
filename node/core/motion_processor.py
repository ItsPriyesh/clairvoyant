import FaBo9Axis_MPU9250
import time
import sys
import os
import math
import RPi.GPIO as GPIO
import clairvoyant_data
from clairvoyant_data import PacketBuilder
from clairvoyant_data import PacketBuilder
import time
import multiprocessing
import clairvoyant


accel_sens = .4 #2*.1
gyro_sens = 50 #250*.1
mag_sens = 10 #10 deg
sample_length = 10



def get_orientation(pitch, roll):
    roll = roll + 180

    if (135<=roll<=225) and (-45<=pitch<=45):
        #print("Top-Up Orientation")
        return 1
    
    elif ((0<=roll<=45) or (315 <= roll <= 360)) and (-45<=pitch<=45):
        #print ("Bottom-Up Orientation")
        return 2

    elif (45<=pitch<=90):
        #print ("Side 1-Up Orientation")
        return 3

    elif (-90<=pitch<=-45):
        #print ("Side 2-Up Orientation")
        return 4

    elif (45<=roll<=135):
        #print ("Side 3-Up Orientation")
        return 5

    elif (225<=roll<=315):
        #print ("Side 4-Up Orientation")
        return 6

    else:
        return 0


def most_frequent(List): 
    return max(set(List), key = List.count)     


def motion(input_buff, output_buff):

    print("Initializing Motion Process....")
    
    #presence sensor
    #pin37 = PWR
    #pin35 = Signal
    GPIO.setwarnings(False)
    
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(37, GPIO.OUT)
    GPIO.output(37, GPIO.HIGH)
    
    GPIO.setup(35, GPIO.IN)
    

    motion_detected = False
    motion_detected_ts = 0

    presence_detected = False
    presence_ts = 0

    accel_x = []
    accel_y = []
    accel_z = []

    gyro_x = []
    gyro_y = []
    gyro_z = []

    mag_x = []
    mag_y = []
    mag_z = []
    
    avg_x = 0
    avg_y = 0
    avg_z = 0

    previous_orientation = 0
    orientation_arr = []

    yaw_arr = []
    avg_yaw = 0


    f = open('motion_calibration.txt','r')
    accel_cal = f.readline()
    accel_cal = accel_cal.rstrip()

    gyro_cal = f.readline()
    gyro_cal = gyro_cal.rstrip()

    mag_cal = f.readline()
    mag_cal = mag_cal.rstrip()

    mag_scale = f.readline()
    mag_scale = mag_scale.rstrip()
    
    f.close()
    
    accel_cal = accel_cal.strip('][').split(', ')
    accel_cal = list(map(float,accel_cal))

    gyro_cal = gyro_cal.strip('][').split(', ')
    gyro_cal = list(map(float,gyro_cal))

    mag_cal = mag_cal.strip('][').split(', ')
    mag_cal = list(map(float,mag_cal))

    mag_scale = mag_scale.strip('][').split(', ')
    mag_scale = list(map(float,mag_scale))

    #print("Calibration Data" + str(accel_cal) + " " + str(gyro_cal))
    

    croll = 0
    cpitch = 0
    gyro_init = False
    old_gts = 0


    mts = 0
    ots = 0
    
    mpu9250 = FaBo9Axis_MPU9250.MPU9250()

    while(1):
        ad = mpu9250.readAccel()

        new_gts = time.time_ns()
        gd = mpu9250.readGyro()
    

        #Remove Offset
        ad['x'] = (0 - accel_cal[0]) + ad['x']
        ad['y'] = (0 - accel_cal[1]) + ad['y']
        ad['z'] = (1 - accel_cal[2]) + ad['z']

        gd['x'] = (0 - gyro_cal[0]) + gd['x']
        gd['y'] = (0 - gyro_cal[1]) + gd['y']
        gd['z'] = (0 - gyro_cal[2]) + gd['z']

        
        apitch = 180*math.atan2(ad['y'],math.sqrt(ad['x']*ad['x']+ad['z']*ad['z']))/math.pi
        aroll = 180*math.atan2(-1*ad['x'],ad['z'])/math.pi

        if (gyro_init == False):
            old_gts = new_gts
            gyro_init = True


        else:
            dt = (new_gts - old_gts)/ (10 ** 9)
            old_gts = new_gts
            #print("time " + str(dt))


            #complementary filter
            croll = .98*(croll + gd['y']*dt) + .02*aroll
            cpitch = .98*(cpitch + gd['x']*dt) + .02*apitch

            if (time.time() - ots > .1):
                ots = time.time()
                get_orientation(cpitch , croll)

                if len(orientation_arr) < sample_length:
                    orientation_arr.append(get_orientation(cpitch , croll))
                else:
                    #has enough samples
                    freq_orr =  most_frequent(orientation_arr)

                    if (freq_orr != previous_orientation) and ((orientation_arr.count(freq_orr))/len(orientation_arr) > 0.8):
                        #more than 60% vals are 1 orientation for the array frame and its diffrent than the previous orientation
                        previous_orientation = freq_orr

                        motion_detected = True

                        

                    orientation_arr.pop(0)
                    orientation_arr.append(get_orientation(cpitch , croll))
                

            if (time.time() - mts > .1):

                md = mpu9250.readMagnet()
                mts = time.time()

                
                md['x'] = ((0 - mag_cal[0]) + md['x'])*mag_scale[0]
                md['y'] = ((0 - mag_cal[1]) + md['y'])*mag_scale[1]
                md['z'] = ((0 - mag_cal[2]) + md['z'])*mag_scale[2]

                pitchRads = math.radians(cpitch)
                rollRads = math.radians(croll)

                #Reassign mag X and Y values in accordance to MPU-9250
                Mx = md['y']
                My = md['x']
                Mz = md['z']

                # Normalize the values
                norm = math.sqrt(Mx * Mx + My * My + Mz * Mz)
                Mx1 = Mx / norm
                My1 = My / norm
                Mz1 = Mz / norm

                # Apply tilt compensation
                Mx2 = Mx1*math.cos(pitchRads) + Mz1*math.sin(pitchRads)
                My2 = Mx1*math.sin(rollRads)*math.sin(pitchRads) + My1*math.cos(rollRads) - Mz1*math.sin(rollRads)*math.cos(pitchRads)
                Mz2 = -Mx1*math.cos(rollRads)*math.sin(pitchRads) + My1*math.sin(rollRads) + Mz1*math.cos(rollRads)*math.cos(pitchRads)

                yaw = 0

                # Heading calculation
                if ((Mx2 > 0) and (My2 >=0)):
                        yaw = math.degrees(math.atan(My2/Mx2))
                elif (Mx2 < 0):
                        yaw = 180 + math.degrees(math.atan(My2/Mx2))
                elif ((Mx2 > 0) and (My2 <= 0)):
                        yaw = 360 + math.degrees(math.atan(My2/Mx2))
                elif ((Mx2 == 0) and (My2 < 0)):
                        yaw = 90
                elif ((Mx2 == 0) and (My2 > 0)):
                        yaw = 270


                #Handle heading
                if len(yaw_arr) < sample_length:
                    yaw_arr.append(yaw)
            
                else:
                    avg_yaw = int(sum(yaw_arr)/len(yaw_arr))
                    yaw_arr.pop(0)
                    yaw_arr.append(yaw)
                    

        #<10 samples
        if len(accel_x) < sample_length:
            accel_x.append(ad['x'])
            accel_y.append(ad['y'])
            accel_z.append(ad['z'])
            
        else:
            #already has 10 samples
            avg_x = sum(accel_x)/len(accel_x)
            avg_y = sum(accel_y)/len(accel_y)
            avg_z = sum(accel_z)/len(accel_z)


            if((ad['x']>=avg_x + accel_sens) or (ad['x']<=avg_x - accel_sens) or \
                (ad['y']>=avg_y + accel_sens) or (ad['y']<=avg_y - accel_sens) or \
                (ad['z']>=avg_z + accel_sens) or (ad['z']<=avg_z - accel_sens)):
                #print("accel movement detected")
                motion_detected = True

                accel_x = []
                accel_y = []
                accel_z = []

            else:
                accel_x.pop(0)
                accel_y.pop(0)
                accel_z.pop(0)

                accel_x.append(ad['x'])
                accel_y.append(ad['y'])
                accel_z.append(ad['z'])

        if len(gyro_x) < sample_length:
            gyro_x.append(gd['x'])
            gyro_y.append(gd['y'])
            gyro_z.append(gd['z'])
            
        else:
            #already has 10 samples
            avg_x = sum(gyro_x)/len(gyro_x)
            avg_y = sum(gyro_y)/len(gyro_y)
            avg_z = sum(gyro_z)/len(gyro_z)


            if((gd['x']>=avg_x + gyro_sens) or (gd['x']<=avg_x - gyro_sens) or \
                (gd['y']>=avg_y + gyro_sens) or (gd['y']<=avg_y - gyro_sens) or \
                (gd['z']>=avg_z + gyro_sens) or (gd['z']<=avg_z - gyro_sens)):
                #print("gyro movement detected")
                motion_detected = True
                

                #reset gyro
                gyro_x = []
                gyro_y = []
                gyro_z = []

            else:
                                                                                                                                               
                gyro_x.pop(0)
                gyro_y.pop(0)
                gyro_z.pop(0)

                gyro_x.append(gd['x'])
                gyro_y.append(gd['y'])
                gyro_z.append(gd['z'])


        #Handle Presence Sensor
        if ((GPIO.input(35) == 1) and (time.time() - presence_ts > 3)):
            presence_ts = time.time()
            presence_detected = True
        
        if (((presence_detected == True) or (motion_detected == True)) and (time.time() - motion_detected_ts > 3)):

            motion_payload = clairvoyant_data.MotionPayload()
            motion_payload._battery_lvl = 100.0
            motion_payload._timestamp = round(time.time())
            
            
            if (presence_detected == True):
                print ("External Motion Detected")
                motion_payload._motion_type = "EXTERNAL"
                presence_detected = False

            if (motion_detected == True):
                print ("Device Motion Detected")
                motion_detected = False
                motion_payload._motion_type = "DEVICE"
                motion_detected_ts = time.time()
            
            if (previous_orientation == 1):
                print("Top-Up Orientation")
                motion_payload._orientation = "TOP"

                
            elif (previous_orientation == 2):
                print ("Bottom-Up Orientation")
                motion_payload._orientation = "BOTTOM"
                
            elif (previous_orientation == 3):
                print ("Side 1-Up Orientation")
                motion_payload._orientation = "SIDE_1"
                
            elif (previous_orientation == 4):
                print ("Side 2-Up Orientation")
                motion_payload._orientation = "SIDE_2"
                
            elif (previous_orientation == 5):
                print ("Side 3-Up Orientation")
                motion_payload._orientation = "SIDE_3"
                
            elif (previous_orientation == 6):
                print ("Side 4-Up Orientation")
                motion_payload._orientation = "SIDE_4"

            motion_payload._roll = croll
            motion_payload._pitch = cpitch
            motion_payload._yaw = avg_yaw
            motion_packet = PacketBuilder().
            

            print("Roll: " + str(int(croll)) + " Pitch: " + str(int(cpitch)))
            

            print("Yaw: " + str(avg_yaw))


            motion_payload = clairvoyant_data.MotionPayload()
            motion_payload._battery_lvl = 100.0
            motion_payload._timestamp = round(time.time())
            motion_packet = PacketBuilder().set_type("MOTION_EVENT").set_node_id(clairvoyant.CURRENT_NODE).set_message_id().set_payload(motion_payload).set_ttl().set_retry_count().set_hop_count()
            built_packet = motion_packet.build()
            output_buff.put(built_packet)

            

