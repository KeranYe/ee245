#!/usr/bin/env python

import math
from math import sin, cos, pi
import numpy as np
from crazyflieParser import CrazyflieParser

if __name__ == '__main__':
    
    index = 1   # for cf1
    initialPosition = [0,0,0] # x,y,z coordinate for this crazyflie
    cfs = CrazyflieParser(index, initialPosition)
    cf = cfs.crazyflies[0]
    time = cfs.timeHelper

    t = np.linspace(0,2*pi,100)
    data = np.array([[0],[1],[1]])
    for i in range(100):
        x = cos(t[i])
        y = sin(t[i])
        current = np.array([[y],[x],[1]])
        data = np.append(data,current,axis =1)
    for i in range(100):
        x = 2 - cos(t[i])
        y = sin(t[i])
        current = np.array([[y],[x],[1]])
        data = np.append(data,current,axis =1)
    data = data.T
    
    cf.setParam("commander/enHighLevel", 1)
    cf.setParam("stabilizer/estimator", 2) # Use EKF
    cf.setParam("stabilizer/controller", 2) # Use mellinger controller
    #cf.setParam("ring/effect", 7)

    cf.takeoff(targetHeight = 0.5, duration = 3.0)
    time.sleep(3.0)

    # FILL IN YOUR CODE HERE
    # Please try both goTo and cmdPosition
    goto_duration = math.sqrt(np.linalg.norm(data[0,:2]))/1.0
    cf.goTo(goal = data[0,:], yaw = 0.0, duration = goto_duration, relative = False, groupMask = 0)
    time.sleep(goto_duration)
    # Move along a segment
    for i in range(200):
        cf.cmdPosition(data[i,:], yaw = 0)
        time.sleep(0.1)

    

    cf.land(targetHeight = 0.0, duration = 5.0)
    time.sleep(5.0)
