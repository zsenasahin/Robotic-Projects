#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry

class YolTakibi:
    def __init__(self):
        rospy.init_node('yol', anonymous=True)
        self.subscriber = rospy.Subscriber('/odom', Odometry, self.callback)
        self.prev_x = 0.0
        self.prev_y = 0.0
        self.total_distance_x = 0.0
        self.total_distance_y = 0.0
        self.is_moving = False  # Hareketin kontrol edilmesi için flag

    def callback(self, msg):
        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y

        # Yol hesaplama
        distance_x = current_x - self.prev_x
        distance_y = current_y - self.prev_y

        self.total_distance_x += distance_x
        self.total_distance_y += distance_y

        self.prev_x = current_x
        self.prev_y = current_y

    def display_distance(self):
        # Hareket ediliyorsa mesafeyi yazdır
        if self.is_moving:
            rospy.loginfo(f"Gidilen Mesafe: X: {self.total_distance_x:.2f}, Y: {self.total_distance_y:.2f}")

    def run(self):
        rate = rospy.Rate(1)  # Her saniye kontrol edilecek
        while not rospy.is_shutdown():
            self.display_distance()
            rate.sleep()

    def set_moving(self, moving):
        self.is_moving = moving

if __name__ == '__main__':
    try:
        yol = YolTakibi()
        # Klavye ile hareket kontrolü için bir döngü
        while not rospy.is_shutdown():
            key = input("Klavye kontrolü için 'w', 'a', 's', 'd' tuşlarını kullanın. Çıkmak için 'q' tuşuna basın: ")
            if key in ['w', 'a', 's', 'd']:
                yol.set_moving(True)  # Hareket ediyor
                yol.run()  # Mesafeyi güncellemeye başla
            elif key == 'q':
                break
            else:
                yol.set_moving(False)  # Hareket etmiyor
                yol.run()  # Mesafeyi güncellemeye devam et
    except rospy.ROSInterruptException:
        pass

