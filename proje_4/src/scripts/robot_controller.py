#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class RobotController:
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        
        self.cmd_msg = Twist()
        self.obstacle_detected = False

        rospy.loginfo("Robot başlıyor!")
        self.control_loop()

    def scan_callback(self, scan_data):
        """LIDAR verilerini işleyerek engel tespiti yapar"""
        front_ranges = scan_data.ranges[0:30] + scan_data.ranges[330:360]  # Ön taraf 60 derece
        min_distance = min(front_ranges) if len(front_ranges) > 0 else float('inf')

        if min_distance < 0.5:  # Engel 0.5 metreden yakınsa
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False

    def avoid_obstacle(self):
        """Engelden kaçınma manevrası"""
        rospy.loginfo("Engel tespit edildi, duruyor ve yön değiştiriyor...")
        
        # Robotu durdur
        self.cmd_msg.linear.x = 0.0
        self.cmd_msg.angular.z = 0.0
        self.cmd_pub.publish(self.cmd_msg)
        rospy.sleep(0.5)
        
        # Sağ tarafa doğru dön
        self.cmd_msg.angular.z = 0.5
        self.cmd_pub.publish(self.cmd_msg)
        rospy.sleep(1.0)
        
        # Düz hareket etmeye devam et
        self.cmd_msg.angular.z = 0.0

    def control_loop(self):
        """Robotun ana kontrol döngüsü"""
        rate = rospy.Rate(10)  # 10 Hz
        
        while not rospy.is_shutdown():
            if self.obstacle_detected:
                self.avoid_obstacle()
            else:
                self.cmd_msg.linear.x = 0.2  # Sabit hızla ilerle
                self.cmd_msg.angular.z = 0.0  # Düz git
            
            self.cmd_pub.publish(self.cmd_msg)
            rate.sleep()

if __name__ == '__main__':
    try:
        RobotController()
    except rospy.ROSInterruptException:
        pass

