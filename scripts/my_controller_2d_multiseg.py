#!/usr/bin/env python

import math
import numpy as np
from crazyflieParser import CrazyflieParser

if __name__ == '__main__':
    
    index = 1   # for cf1
    initialPosition = [0,1.5,0] # x,y,z coordinate for this crazyflie
    cfs = CrazyflieParser(index, initialPosition)
    cf = cfs.crazyflies[0]
    time = cfs.timeHelper

    # Get input for segments
    num_seg = int(raw_input("Number of segments:"))
    takeoff_height = float(raw_input("takeoff height:"))  
    takeoff_duration = float(raw_input("takeoff duration:"))
    wp_list = np.zeros((num_seg,3)) # list of way point 
    duration_list = np.zeros((num_seg,1)) # list of duration
    for i in range(num_seg):
        wp_list[i,:] = map(float, raw_input("x,y,z = ").split())
        duration_list[i,0] = float(raw_input("duration:"))
    
    cf.setParam("commander/enHighLevel", 1)
    cf.setParam("stabilizer/estimator", 2) # Use EKF
    cf.setParam("stabilizer/controller", 2) # Use mellinger controller
    #cf.setParam("ring/effect", 7)

    cf.takeoff(targetHeight = takeoff_height, duration = takeoff_duration)
    time.sleep(takeoff_duration)

    # FILL IN YOUR CODE HERE
    # Please try both goTo and cmdPosition
    #cf.goTo(goal = np.array([2,2,2]), yaw = 0.0, duration = 3.0, relative = False, groupMask = 0)
    #time.sleep(3.0)
    # Move along a segment
    for i in range(num_seg):
        cf.goTo(goal = wp_list[i,:], yaw = 0.0, duration = duration_list[i,0], relative = False, groupMask = 0)
        time.sleep(duration_list[i,0])

    

    cf.land(targetHeight = 0.0, duration = 5.0)
    time.sleep(5.0)
