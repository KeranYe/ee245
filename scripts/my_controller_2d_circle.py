#!/usr/bin/env python

import math
import numpy as np
from crazyflieParser import CrazyflieParser

def PointsInCircum(r,n=100):
    return [[math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r] for x in range(0,n+1)]

if __name__ == '__main__':
    pi = math.pi
    index = 1   # for cf1
    initialPosition = [0,0,0] # x,y,z coordinate for this crazyflie
    cfs = CrazyflieParser(index, initialPosition)
    cf = cfs.crazyflies[0]
    time = cfs.timeHelper

    # Get input for circle
    num_wp = 100    
    takeoff_height = float(raw_input("takeoff height:"))  
    takeoff_duration = float(raw_input("takeoff duration:"))
    center = map(float, raw_input("x,y of center= ").split())
    #print np.shape(center)
    radius = math.sqrt(np.linalg.norm(center))
    circle = PointsInCircum(radius,n = num_wp)
    circle = np.reshape(circle, (-1,2))
    wp_list = circle + center
    #print np.shape(wp_list)
    #wp_list = np.reshape(wp_list, (-1,2))
    z_list = takeoff_height*(np.ones((num_wp+1,1)))
    wp_list = np.append(wp_list, z_list, axis = 1)
    
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
    goto_duration = math.sqrt(np.linalg.norm(wp_list[0,:2]))/1.0
    cf.goTo(goal = wp_list[0,:], yaw = 0.0, duration = goto_duration, relative = False, groupMask = 0)
    time.sleep(goto_duration)
    for i in range(num_wp+1):
        cf.cmdPosition(wp_list[i,:], yaw = 0)
        time.sleep(0.1)

    

    cf.land(targetHeight = 0.0, duration = 5.0)
    time.sleep(5.0)
