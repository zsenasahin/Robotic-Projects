#!/usr/bin/env python3
import rospy
import requests
from std_msgs.msg import String

def get_weather():
    api_key = "864142924826b92f56723cd502808e40"
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Konya&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temp = data['main']['temp']
        rospy.loginfo(f"Konya'nın sıcaklığı: {temp}°C")
        return f"Konya'nın sıcaklığı: {temp}°C"
    else:
        rospy.logwarn("Hava durumu verisi alınamadı.")
        return "Hava durumu verisi alınamadı."

def publish_weather():
    rospy.init_node('hava', anonymous=True)
    pub = rospy.Publisher('/konya_sicaklik', String, queue_size=10)
    rate = rospy.Rate(1)  # Her 1 saniyede bir hava durumu güncellemesi
    while not rospy.is_shutdown():
        weather_info = get_weather()
        pub.publish(weather_info)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_weather()
    except rospy.ROSInterruptException:
        pass

