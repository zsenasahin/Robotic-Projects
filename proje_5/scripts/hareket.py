#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import threading

def get_key():
    """Klavye girişini almak için fonksiyon"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def hareket():
    rospy.init_node('hareket', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)

    hareket = Twist()

    # 1. 5 saniye ileri git
    hareket.linear.x = 0.1
    hareket.angular.z = 0.0
    rospy.loginfo("İleri gidiyor...")
    for _ in range(50):
        pub.publish(hareket)
        rate.sleep()

    # 2. 90 derece sola dön
    hareket.linear.x = 0.0
    hareket.angular.z = 0.5
    rospy.loginfo("Sola dönüyor...")
    duration = 1.57 / 0.5
    start_time = rospy.get_time()
    while rospy.get_time() - start_time < duration:
        pub.publish(hareket)
        rate.sleep()

    # 3. 5 saniye geri git
    hareket.angular.z = 0.0
    hareket.linear.x = -0.1
    rospy.loginfo("Geri gidiyor...")
    for _ in range(50):
        pub.publish(hareket)
        rate.sleep()

    # 4. 90 derece sağa dön
    hareket.linear.x = 0.0
    hareket.angular.z = -0.5
    rospy.loginfo("Sağa dönüyor...")
    duration = 1.57 / 0.5
    start_time = rospy.get_time()
    while rospy.get_time() - start_time < duration:
        pub.publish(hareket)
        rate.sleep()

    # 5. 5 saniye daha ilerle
    hareket.angular.z = 0.0
    hareket.linear.x = 0.1
    rospy.loginfo("İleri gidiyor...")
    for _ in range(50):
        pub.publish(hareket)
        rate.sleep()

    # 6. 135 derece sola dön
    hareket.linear.x = 0.0
    hareket.angular.z = 0.5
    rospy.loginfo("Sola dönüyor...")
    duration = 2.356 / 0.5
    start_time = rospy.get_time()
    while rospy.get_time() - start_time < duration:
        pub.publish(hareket)
        rate.sleep()

    # 7. 5 saniye daha ilerle
    hareket.angular.z = 0.0
    hareket.linear.x = 0.1
    rospy.loginfo("İleri gidiyor...")
    for _ in range(50):
        pub.publish(hareket)
        rate.sleep()

    # Robotu durdur
    hareket.linear.x = 0.0
    hareket.angular.z = 0.0
    pub.publish(hareket)
    rospy.loginfo("Hareket tamamlandı, robot durdu.")

    # Klavye ile kontrol için bir döngü başlat
    rospy.loginfo("Klavye ile kontrol için 'w', 'a', 's', 'd' tuşlarını kullanın. Çıkmak için 'q' tuşuna basın.")
    while not rospy.is_shutdown():
        key = get_key()
        if key == 'w':
            hareket.linear.x = 0.1
            hareket.angular.z = 0.0
        elif key == 's':
            hareket.linear.x = -0.1
            hareket.angular.z = 0.0
        elif key == 'a':
            hareket.linear.x = 0.0
            hareket.angular.z = 0.5
        elif key == 'd':
            hareket.linear.x = 0.0
            hareket.angular.z = -0.5
        elif key == 'q':
            break
        else:
            hareket.linear.x = 0.0
            hareket.angular.z = 0.0

        pub.publish(hareket)
        rospy.loginfo(f"Klavyeden kontrol: X: {hareket.linear.x}, Y: {hareket.angular.z}")  # Pose bilgisi
        rate.sleep()

    # Robotu durdur
    hareket.linear.x = 0.0
    hareket.angular.z = 0.0
    pub.publish(hareket)
    rospy.loginfo("Robot durdu.")

if __name__ == '__main__':
    try:
        hareket()
    except rospy.ROSInterruptException:
        pass

