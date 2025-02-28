#!/usr/bin/env python3
import rospy
from ros_tutorials.msg import IoTSensor
import datetime

# Başlangıç koordinatları
x, y, z = 1, 1, 1

# Hedef koordinatlar
target_x, target_y, target_z = 7, 7, 1

pub = rospy.Publisher('robot_coordinates_topic', IoTSensor, queue_size=10)

# ROS düğümünü başlatma
rospy.init_node('robot_publisher_node', anonymous=True)

rate = rospy.Rate(1)  # 1 Hz

while not rospy.is_shutdown():
    iot_sensor = IoTSensor()
    iot_sensor.id = 1
    iot_sensor.name = "robot_01"
    
    x += 1
    y += 1
    
    iot_sensor.temperature = x  
    iot_sensor.humidity = y  
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rospy.loginfo(f"[{current_time}] Yayımlanan veri: ID: {iot_sensor.id}, "
                  f"Name: {iot_sensor.name}, X: {iot_sensor.temperature}, "
                  f"Y: {iot_sensor.humidity}, Z: {z}")

    pub.publish(iot_sensor)
    
    # Hedefe ulaşıldı mı kontrolü
    if x == target_x and y == target_y and z == target_z:
        rospy.loginfo("Robot hedefe ulaştı!")
        break  # Hedefe ulaşıldığında döngüyü sonlandır

    # Yayın döngüsünü bekletiyoruz (1 saniye)
    rate.sleep()

