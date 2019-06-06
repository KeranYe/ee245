#!/usr/bin/env python

import math
from math import sin, cos, pi
import numpy as np
from crazyflieParser import CrazyflieParser

def eight_traj():
    t = np.linspace(0,2*pi,100)
    data = np.array([[0],[1],[1]])
    for i in range(100):
        x = 0.5*cos(t[i])
        y = 0.5*sin(t[i])
        current = np.array([[y],[x],[1]])
        data = np.append(data,current,axis =1)
    for i in range(100):
        x = 1 - 0.5*cos(t[i])
        y = 0.5*sin(t[i])
        current = np.array([[y],[x],[1]])
        data = np.append(data,current,axis =1)
    data = data.T
    return data

if __name__ == '__main__':
    
    index = 1   # for cf1
    initialPosition = [0.0, 1.5, 0.0] # x,y,z coordinate for this crazyflie
    cfs = CrazyflieParser(index, initialPosition)
    cf = cfs.crazyflies[0]
    time = cfs.timeHelper
    
    # Get input for eight trajectory
    eight_traj = eight_traj()
   
    cf.setParam("commander/enHighLevel", 1)
    cf.setParam("stabilizer/estimator", 2) # Use EKF
    cf.setParam("stabilizer/controller", 2) # Use mellinger controller
    #cf.setParam("ring/effect", 7)    
    
    # Takeoff
    cf.takeoff(targetHeight = 1, duration = 5.0)
    time.sleep(5.0)
    
    # GO to the first point of eight trajectory
    cf.goTo(goal = eight_traj[0,:], yaw = 0.0, duration = 5.0, relative = False, groupMask = 0)
    time.sleep(5.0)
    
    # Move along eight trajectory
    for i in range(200):
        cf.cmdPosition(eight_traj[i,:], yaw = 0)
        time.sleep(0.1)

    # Go back to landing
    cf.goTo(goal = [0.0, 1.5, 1.0], yaw = 0.0, duration = 5.0, relative = False, groupMask = 0)
    time.sleep(5.0)

    cf.land(targetHeight = 0.0, duration = 5.0)
    time.sleep(5.0)
