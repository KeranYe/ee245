#!/usr/bin/env python

import math
from math import sin, cos, pi
import numpy as np
from crazyflieParser import CrazyflieParser

def eight_traj():
    t = np.linspace(0,2*pi,101)
    data = np.array([[0],[1],[2]])
    for i in range(1,101):
        y = cos(t[i])
        x = sin(t[i])
        current = np.array([[x],[y],[2*(1+0.15*(cos(t[i])-1)+0.15*sin(t[i]))]])
        data = np.append(data,current,axis =1)
    for i in range(101):
        y = 2 - cos(t[i])
        x = sin(t[i])
        current = np.array([[x],[y],[2*(1-0.15*(cos(t[i])-1)+0.15*sin(t[i]))]])
        data = np.append(data,current,axis =1)
    data = data.T
    data = data + np.array([0, -1, 0])
    data = 0.5 * data
    return data

if __name__ == '__main__':
    
    index = 1   # for cf1
    initialPosition = [0.0, 1.5, 0.0] # x,y,z coordinate for this crazyflie
    cfs = CrazyflieParser(index, initialPosition)
    cf = cfs.crazyflies[0]
    time = cfs.timeHelper
    
    # Get input for eight trajectory
    traj = eight_traj()
   
    cf.setParam("commander/enHighLevel", 1)
    cf.setParam("stabilizer/estimator", 2) # Use EKF
    cf.setParam("stabilizer/controller", 2) # Use mellinger controller
    #cf.setParam("ring/effect", 7)    
    
    # Takeoff
    cf.takeoff(targetHeight = 1, duration = 5.0)
    time.sleep(5.0)
    
    # GO to the first point of eight trajectory
    cf.goTo(goal = traj[0,:], yaw = 0.0, duration = 5.0, relative = False, groupMask = 0)
    time.sleep(5.0)
    
    # Move along eight trajectory
    for i in range(0,202):
        cf.cmdPosition(traj[i,:], yaw = 0)
        time.sleep(0.1)

    # Go back to landing
    cf.goTo(goal = [0.0, 1.5, 1.0], yaw = 0.0, duration = 5.0, relative = False, groupMask = 0)
    time.sleep(5.0)

    cf.land(targetHeight = 0.0, duration = 5.0)
    time.sleep(5.0)
