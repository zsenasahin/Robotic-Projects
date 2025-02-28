#!/usr/bin/env python3

import sys
import rospy
from ros_tutorials.srv import CalcRectangleArea
from ros_tutorials.srv import CalcRectangleAreaRequest
from ros_tutorials.srv import CalcRectangleAreaResponse

def calc_rectangle_area_client(width, height):
    rospy.wait_for_service('calc_rectangle_area')
    try:
        calc_rectangle_area = rospy.ServiceProxy('calc_rectangle_area', CalcRectangleArea)
        resp1 = calc_rectangle_area(width, height)
        return resp1.area
    except rospy.ServiceException as e:
        print ("Service call failed: %s"%e)

def usage():
    return 

if __name__ == "__main__":
    if len(sys.argv) == 3:
        width = float(sys.argv[1])
        height = float(sys.argv[2])
    else:
        print ("%s [width height]"%sys.argv[0])
        sys.exit(1)
    print ("Requesting area of rectangle with width=%s and height=%s"%(width, height))
    area = calc_rectangle_area_client(width, height)
    print ("The area of the rectangle with width %s and height %s is %s"%(width, height, area))

