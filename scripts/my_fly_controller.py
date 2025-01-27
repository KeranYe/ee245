#!/usr/bin/env python

import math
import numpy as np
from crazyflieParser import CrazyflieParser

if __name__ == '__main__':
    
    index = 1   # for cf1
    initialPosition = [0,0,0] # x,y,z coordinate for this crazyflie
    cfs = CrazyflieParser(index, initialPosition)
    cf = cfs.crazyflies[0]
    time = cfs.timeHelper
    
    cf.setParam("commander/enHighLevel", 1)
    cf.setParam("stabilizer/estimator", 2) # Use EKF
    cf.setParam("stabilizer/controller", 2) # Use mellinger controller
    #cf.setParam("ring/effect", 7)
    
    # Get input for segments
    num_seg = int(raw_input("Number of segments:"))
    takeoff_height = float(raw_input("takeoff height"))
    wp_list = np.array([]) # list of way point    
    for i in range(num_seg):
        wp_list[]
    
    traj_duration = 5
    num_wp = int(traj_duration * 10)
    height = 0.5
    x_list = np.reshape(np.linspace(0,2,num_wp),(-1,1))
    y_list = np.reshape(np.linspace(0,2,num_wp),(-1,1))
    z_list = np.reshape(np.linspace(height,2,num_wp),(-1,1))
    pos_list = np.append(x_list, y_list, axis = 1)
    pos_list = np.append(pos_list, z_list, axis = 1)

    cf.takeoff(targetHeight = height, duration = 3.0)
    time.sleep(3.0)

    # FILL IN YOUR CODE HERE
    # Please try both goTo and cmdPosition
    #cf.goTo(goal = np.array([2,2,2]), yaw = 0.0, duration = 3.0, relative = False, groupMask = 0)
    #time.sleep(3.0)
    # Move along a segment
    for i in range(num_wp):
        cf.cmdPosition(pos_list[i,:], yaw = 0)
        time.sleep(0.1)

    

    cf.land(targetHeight = 0.0, duration = 5.0)
    time.sleep(5.0)
