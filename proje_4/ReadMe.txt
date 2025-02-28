					## Turtlebot3 robot simülasyonu ##
					
** Projenin Özeti **

Bu proje, gazebo ortamında bir turtlebot3 robotunun belirli bir noktadan harekete başlar, karşısına bir engel çıkana kadar harekete devam eder. Karşısına engel çıktığında ise durur, yön değiştirir (önünde engel olmayana kadar döner) ve harekete devam eder. 
Robot, `robot_controller.py` adlı Python dosyası ile kontrol edilir ve bir ROS `launch` dosyası ile çalıştırılır.

** Proje Gereksinimleri **

- ROS (Robot Operating System)
- TurtleBot3 Paketi
- Gazebo Simülasyon Ortamı
- Python 3.x

** Dosya Yapısı **

-> robot_simulation.launch: Simülasyon ortamını başlatmak ve robot kontrolünü etkinleştirmek için kullanılan launch dosyası.
-> robot_controller.py: Robotun hareket algoritmalarını ve engelden kaçınma davranışını içeren Python dosyası.


** Adım adım kurulum ve çalıştırma **

1. Catkin Workspace Oluşturma
Eğer bir catkin_ws çalışma alanınız yoksa oluşturun: (terminali açıp aşağıdaki kodu yazıyoruz)

mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make

2. Paket Oluşturma
Yeni bir ROS paketi oluşturun:
cd ~/catkin_ws/src
catkin_create_pkg vize_sonrasi_odev rospy std_msgs geometry_msgs sensor_msgs

3. Python kodu için scripts klasörü ve py dosyasını oluşturma
Paketin scripts klasörünü oluşturun ve robot_controller.py adında bir dosya oluşturun:

cd ~/catkin_ws/src/vize_sonrasi_odev
mkdir scripts
cd scripts
touch robot_controller.py

4. Launch dosyası için klasör ve .launch uzantılı dosyayı oluşturma
launch klasörünü oluşturun ve robot_simulation.launch adında bir dosya ekleyin:

cd ~/catkin_ws/src/vize_sonrasi_odev
mkdir launch
cd launch
touch robot_simulation.launch

NOT: launch dosyasına çalıştırmayı istediğimiz şeyleri yazıyoruz. örneğin ben turtlebot3_world dünyasında bir gazebo açmak ve rviz çalıştırmak istediğim için şu kodları yazdım:
<launch>
    <!-- Gazebo boş bir dünya başlat -->
  <include file="$(find turtlebot3_gazebo)/launch/turtlebot3_world.launch"/>
  
    <!-- Rviz'i başlat -->
    <include file="$(find turtlebot3_gazebo)/launch/turtlebot3_gazebo_rviz.launch"/>

    <!-- Robot kontrol node'unu çalıştır -->
    <node name="robot_controller" pkg="vize_sonrasi_odev" type="robot_controller.py" output="screen"/>

</launch>


5. CMakeLists.txt dosyamızda kullandığımız yerleri yorum satırından çıkarıyoruz. örneğin:
catkin_package(
  INCLUDE_DIRS include
  LIBRARIES vize_sonrasi_odev
  CATKIN_DEPENDS roscpp rospy std_msgs
  DEPENDS system_lib
)

 generate_messages(
   DEPENDENCIES
   std_msgs
 )

6. ve son adım olarak dosyalarımızı derlememiz gerekiyor. bunun için terminale cd ~/catkin_ws yazıp workspacemizin içie geliyoruz ve catkin_make yazıyoruz. bu derleme bittikten sonra yapmamız gereken tek şey terminale gidip launch dosyamızı çalıştırmak olacak.

7. Terminale gidip şu kodu yazıyoruz:
roslaunch vize_sonrasi_odev robot_simulation.launch

bunu yazdıktan sonra otomatik olarak gazebo açılacak ve robot harekete başlayacaktır. ben launch dosyamda rviz de çalıştırdığım için gazebo ile birlikte rviz de açılacak.

Ek Bilgi rviz de çıkan ekranda camera seçeneğini eklerseniz robotun kamerasını aktif edip robot gözünden dünyayı görebilirsiniz!



