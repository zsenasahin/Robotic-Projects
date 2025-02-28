#!/usr/bin/env python3

import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class FindNearestWall:
    def __init__(self):
        rospy.init_node('find_nearest_wall', anonymous=True)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)

        self.rate = rospy.Rate(10)
        self.min_distance = float('inf')
        self.min_angle = None
        self.laser_data = []
        self.safe_distance = 0.379  # Duvara yaklaşırken bırakılacak güvenli mesafe

    def laser_callback(self, msg):
        self.laser_data = msg.ranges

    def rotate(self, angular_speed):
        vel_msg = Twist()
        vel_msg.angular.z = angular_speed
        self.vel_pub.publish(vel_msg)

    def stop(self):
        vel_msg = Twist()
        self.vel_pub.publish(vel_msg)

    def move_towards_wall(self):
        rospy.loginfo("Moving towards the nearest wall")
        vel_msg = Twist()
        vel_msg.linear.x = 0.2  # Düşük hızda ilerliyoruz, çarpma olmasın

        # Robot, güvenli mesafeye kadar ilerlesin
        while not rospy.is_shutdown():
            # Lazer verilerini kontrol et
            min_distance_in_front = min(self.laser_data[0:30] + self.laser_data[-30:])  # Ön taraftaki mesafeleri kontrol et
            if min_distance_in_front > self.safe_distance:
                self.vel_pub.publish(vel_msg)
            else:
                rospy.loginfo("Reached safe distance from the wall. Stopping.")
                self.stop()
                break

            self.rate.sleep()

    def start(self):
        rospy.loginfo("Finding the nearest wall...")

        # 360 derece dön
        self.min_distance = float('inf')
        for _ in range(36):  # 360 dereceyi 10 derece aralıklarla tarıyoruz
            self.rotate(math.pi / 18)  # 10 derece dönecek
            self.rate.sleep()

        self.stop()

        # Lazer verilerini analiz et ve en yakın duvarı bul
        for i, distance in enumerate(self.laser_data):
            if distance < self.min_distance and distance > 0.5:  # 0.5 metreden daha yakın olan verileri göz ardı et
                self.min_distance = distance
                self.min_angle = i

        rospy.loginfo(f"Nearest wall at angle: {self.min_angle} degrees, Distance: {self.min_distance:.2f} meters")

        # Hedef duvara doğru dönebilmek için açıyı hesapla
        target_angle = self.min_angle * math.pi / 180  # Dereceyi radiana çevir

        rospy.loginfo(f"Target angle: {math.degrees(target_angle):.2f} degrees")

        # Duvara doğru dönme işlemi
        vel_msg = Twist()
        vel_msg.angular.z = 0.5 if target_angle > 0 else 0.5  # Doğru yönde dönmesini sağla
        rotation_time = abs(target_angle) / 0.5  # Dönme süresi

        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < rotation_time:
            self.vel_pub.publish(vel_msg)
            self.rate.sleep()

        self.stop()

        # Hedef duvara doğru düzgün gitme işlemi
        self.move_towards_wall()
        
        # Temp noktasını ROS parametre olarak yayınla
        rospy.set_param('/temp_coordinates', (self.min_distance, target_angle))

        # INFO mesajını logla
        rospy.loginfo("ROBOT EN YAKIN DUVARA GELDİ, 2. KISIM BAŞLIYOR")

if __name__ == '__main__':
    try:
        finder = FindNearestWall()
        finder.start()
    except rospy.ROSInterruptException:
        pass

