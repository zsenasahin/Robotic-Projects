#!/usr/bin/env python3

from ros_tutorials.srv import CalcRectangleArea
from ros_tutorials.srv import CalcRectangleAreaRequest
from ros_tutorials.srv import CalcRectangleAreaResponse

import rospy

def handle_calc_rectangle_area(req):
    area = req.width * req.height
    print ("Returning [Area = %s * %s = %s]"%(req.width, req.height, area))
    return CalcRectangleAreaResponse(area)

def calc_rectangle_area_server():
    rospy.init_node('calc_rectangle_area_server')
    s = rospy.Service('calc_rectangle_area', CalcRectangleArea, handle_calc_rectangle_area)
    print ("Ready to calculate the area of a rectangle.")
    rospy.spin()
    
if __name__ == "__main__":
    calc_rectangle_area_server()

