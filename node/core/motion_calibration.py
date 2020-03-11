import FaBo9Axis_MPU9250
import time
import sys
import os



a = input("Press enter when ready to calibrate. Don't move Device")
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
calibration_samples = 500
calibration_step = 0
ts = 0

mpu9250 = FaBo9Axis_MPU9250.MPU9250()
open('motion_calibration.txt', 'w').close()
f = open('motion_calibration.txt','w')

while(1):
    ad = mpu9250.readAccel()
    gd = mpu9250.readGyro()
    md = mpu9250.readMagnet()

    if calibration_step == 0:

        #<10 samples
        if len(accel_x) < calibration_samples:
            accel_x.append(ad['x'])
            accel_y.append(ad['y'])
            accel_z.append(ad['z'])

            gyro_x.append(gd['x'])
            gyro_y.append(gd['y'])
            gyro_z.append(gd['z'])

            mag_x.append(md['x'])
            mag_y.append(md['y'])
            mag_z.append(md['z'])
            
        else:
            #already has n samples
            avg_x = sum(accel_x)/len(accel_x)
            avg_y = sum(accel_y)/len(accel_y)
            avg_z = sum(accel_z)/len(accel_z)
            avg_list_accel = [avg_x,avg_y,avg_z]

            avg_x = sum(gyro_x)/len(gyro_x)
            avg_y = sum(gyro_y)/len(gyro_y)
            avg_z = sum(gyro_z)/len(gyro_z)
            avg_list_gyro = [avg_x, avg_y, avg_z]

            avg_x = sum(mag_x)/len(mag_x)
            avg_y = sum(mag_y)/len(mag_y)
            avg_z = sum(mag_z)/len(mag_z)
            avg_list_mag = [avg_x, avg_y, avg_z]

            
            f.write(str(avg_list_accel) + "\n")
            f.write(str(avg_list_gyro) + "\n")
            f.write(str(avg_list_mag) + "\n")

            calibration_step = 1
            mag_x = []
            mag_y = []
            mag_z = []
            

            input("Done Initial Cal, Move Device in Figure 8 until next prompt, approx 15 seconds")
            print("Calibrating",end='')
            ts = time.time()
            
            
    if calibration_step == 1:
        mag_x.append(md['x'])
        mag_y.append(md['y'])
        mag_z.append(md['z'])
        
        if (time.time() - ts) > 15:
            print("")
            chord_x = (max(mag_x) - min(mag_x))/2
            chord_y = (max(mag_y) - min(mag_y))/2
            chord_z = (max(mag_z) - min(mag_z))/2

            chord_avg = (chord_x + chord_y + chord_z)/3
            
            mag_xs = chord_avg/chord_x
            mag_ys = chord_avg/chord_y
            mag_zs = chord_avg/chord_z

            mag_scale = [mag_xs, mag_ys, mag_zs]
            f.write(str(mag_scale) + "\n")
            f.close()
            print("done calibrating")
            break

        
                    
        
