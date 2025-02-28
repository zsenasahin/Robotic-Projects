#!/usr/bin/env python3
import rospy
from ros_tutorials.msg import IoTSensor
import datetime

# Hedef koordinatlar
target_x, target_y, target_z = 7, 7, 1

def robot_callback(robot_position):
    x = robot_position.temperature  
    y = robot_position.humidity  
    z = 1  # z koordinatı sabit
    
    # Saat bilgisini alıyoruz
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Gelen mesajları ve koordinatları terminale yazdırıyoruz
    rospy.loginfo(f"[{current_time}] Gelen robot koordinatları: X: {x}, Y: {y}, Z: {z}")
    
    # Hedefe ulaşılıp ulaşılmadığını kontrol ediyoruz
    if round(x) == target_x and round(y) == target_y and z == target_z:
        rospy.loginfo("Robot hedefe ulaştı!")

# ROS düğümünü başlatıyoruz
rospy.init_node('robot_subscriber_node', anonymous=True)

# Subscriber'ı başlatıyoruz
rospy.Subscriber("robot_coordinates_topic", IoTSensor, robot_callback)

# ROS spin fonksiyonu, düğümü durmadan çalıştırır
rospy.spin()

