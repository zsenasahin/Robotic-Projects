HOUSE DÜNYASINDA ROBOT İLE HARİTAYI AÇMA VE HARİTA ÜZERİNDEN 3 NOKTA ARASINDA İLERLEME

=> ÖNCELİKLE ÖDEVİMİZİN NE OLDUĞUNA BAKALIM.
TURTLEBOT3_HOUSE DÜNYASINDA GAZEBO AÇIYORUZ VE BURADA HARİTAYI GEZEREK TÜM ALANLARI AÇIYORUZ. DAHA SONRA BU HARİTAYI TERMİNALDE YAZDIĞIMIZ KOD İLE PAKETİMİZİN İÇİNE KAYDEDİYORUZ.
DAHA SONRA BİR PYTHON KODU İLE ROBOTUMUZUN RASTGELE BELİRLEDİĞİMİZ ÜÇ NOKTA ARASINDA GİTMESİNİ SAĞLIYORUZ. HAREKET ETMESİ İÇİNDE AZ ÖNCE KAYDETTİĞİMİZ HARİTAYI KULLANIYORUZ.

SÖZEL OLDUĞU İÇİN ANLAŞILMAMIŞ OLABİLİR ŞİMDİ BİRDE BUNU SOMUTLAŞTIRARAK YANİ KOMUTLAR İLE ANLATAYIM.

****** ADIM 1 ******

İLK ÖNCE WORKSPACE İÇERİSİNE PAKET OLUŞTURUYORUZ. ÖRNEĞİN BENİM WORKSPACE'MİN ADI: "Catkin_ws" . PAKET OLUŞTURMAK İÇİN TERMİNAL KULLANIYORUZ. MASAÜSTÜNE SAĞ TIKLAYIP "OPEN İN TERMİNAL" DİYORUZ. KÜÇÜK BİR EKRAN AÇILACAK. BU EKRANA ŞU KOMUTLARI YAZIYORUZ. 
komut1:  cd ~/catkin_ws 
bu komut sayesinde workspace içerisine girmiş olduk..
ŞİMDİ BURAYA PAKET OLUŞTURMAK İÇİN ŞU KOMUTU YAZIYORUZ:
komut2: catkin_create_pkg odev2_map std_msgs rospy roscpp

BU KOMUT DA odev2_map YAZDIĞIM KENDİ PAKET ADIM. SİZ BURAYA RASTGELE PAKET ADI VEREBİLİRSİNİZ.

DAHA SONRA CMakeList.txt DOSYAMIZDA BAZI KISIMLARI YORUM SATIRINDAN ÇIKARMAMIZ GEREKİYOR. (yorum satırı dediğimiz şey satırın başında # olduğu zaman o satırın yorum satırında olması demektir. yorum satırından çıkarmak için de # işaretini sileriz)

BU SATIRLAR ŞUNLAR:
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

 generate_messages(
   DEPENDENCIES
   std_msgs
 )
 
 catkin_package(
  INCLUDE_DIRS include
  LIBRARIES odev2_map
  CATKIN_DEPENDS roscpp rospy std_msgs
  DEPENDS system_lib
)

BU SATIRLARI YORUM SATIRINDAN ÇIKARDIKTAN SONRA package.xml DOSYAMIZDA DA 61. SATIRA ŞUNU EKLİYORUZ:
  <exec_depend>message_runtime</exec_depend>


SON OLARAK BÜTÜN YAPTIKLARIMIZI DERLEMEK İÇİN TEKRAR TERMİNALİ AÇIYORUZ. VE SIRASIYLA ŞU KOMUTLARI YAZIYORUZ:
cd ~/catkin_ws  (burada catkin_ws yerine kendi workspace adını yazabilirsiniz)
catkin_make (bu tüm paketi derlemenizi sağlar)

ADIM 1 DE YAPACAKLARIMIZ BU KADAR..

****** ADIM 2 ******
ŞİMDİ AZ ÖNCEKİ TERMİNALİ KAPATIP YENİ BİR TERMİNAL AÇALIM. BURADA ROS BAŞLATMAK İÇİN TERMİNALE ŞU KOMUTU YAZMAMIZ LAZIM:
komut1: roscore
BU KOMUTU ASLA KAPATMAMAMIZ GEREKİYOR. KAPATIRSAK PROGRAM SONLANIR. 

ŞİMDİ YENİ BİR TERMİNAL AÇIYORUZ VE BU TERMİNALE DE ŞU KOMUTU YAZIYORUZ:
komut2: roslaunch turtlebot3_gazebo turtlebot3_house.launch

BU SAYEDE GAZEBO DA HOUSE ORTAMINDA ROBOTUMUZ GÖZÜKECEK.

TEKRAR YENİ BİR TERMİNAL AÇIP ŞU KOMUTU YAZIYORUZ:
komut3: roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping

BU KOMUT İLE RVİZ DİYE BİR YER AÇILACAK VE ORADA ROBOTUMUZ GÖZÜKECEK. FAKAT HARİTA TAM OLARAK AÇIK OLMAYACAK. KLAVYEDEN HAREKET ETTİREREK TÜM HARİTAYI AÇIP BİR YERE KAYDETMEMİZ GEREKİYOR
KLAVYEDEN HAREKET İÇİN DE ŞU KODU YAZMAMIZ GEREKİYOR:
komut4: roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
BU KOMUTU YAZDIĞIMIZDA HALA TERMİNAL EKRANINDAYKEN W A S D X TUŞLARI İLE ROBOTU HAREKET ETTİREBİLİRİZ.
W: İLERİ
A: SOL
D: SAĞ
X: GERİ
S: DURDURMA

-------

****** ADIM 3 ******

DAHA SONRA HARİTAYI TAMAMEN GEZEREK ÇIKARTTIKTAN SONRA BU HARİTAYI ŞU KOMUTLA KAYDEDERİZ:
komut5: rosrun map_server map_saver -f ~/catkin_ws/src/odev2_map/map

BU KOMUT HARİTAYI VE HARİTANIN .yaml UZANTILI KODLARINI PAKETİMİZİN İÇERİSİNDEKİ MAP KLASÖRÜNÜN İÇİNE KAYDEDER.

DAHA SONRA .yaml UZANTILI DOSYANIN ÜZERİNDE SAĞ TIKLAYIP PROPERTİES DİYİP ORDAKİ DOSYA YOLUNU ALIRIZ. BU BİZİM HARİTAMIZIN DOSYA YOLUDUR. DAHA SONRAKİ AŞAMALARDA BU DOSYA YOLUNU KULLANIRIZ.

-------

****** ADIM 4 ******
ŞİMDİ HARİTAMIZI OLUŞTURMUŞ VE KAYDETMİŞ OLDUK. DAHA SONRA ROBOTUN RASTGELE 3 NOKTA ARASINDA GEZMESİ İÇİN BİR PYTHON KODU YAZMAMIZ GEREKİYOR. BENİM YAZDIĞIM PYTHON KODU PAKETİN İÇERİSİNDEKİ SRC İÇERİSİNDE navigate_goal.py ADLI DOSYADADIR ORADAN İNCELEYEBİLİRSİNİZ.

BURADA 3 NOKTA OLMASI İÇİN ŞU KISMI EKLEDİK:
rospy.init_node('map_navigation', anonymous=False)
   x_goal = 0
   y_goal = -2
   print('start go to goal')
   move_to_goal(x_goal,y_goal)
   
   x2_goal = -3
   y2_goal = 0
   print('start go to goal')
   move_to_goal(x_goal,y_goal)
   
   x3_goal = 0
   y3_goal = 1
   print('start go to goal')
   move_to_goal(x_goal,y_goal)


BU SAYEDE ROBOT 3 NOKTA ARASINDA GEZEBİLECEK.

komut7: roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/home/zeynepsena/catkin_ws/src/ros_course_part2-master/src/topic03_map_navigation/tb3map/tb3_house_map_yaml

BURAYI DA ÇALIŞTIRDIĞIMIZDA RVİZ AÇILACAK VE ROBOTUN HAREKETLERİNİ ORDAN DA GÖREBİLİCEZ.

DAHA SONRA BU PYTHON KODUNU ÇALIŞTIRMAK İÇİN İSE ŞU KOMUTU YAZIYORUZ (YİNE FARKLI BİR TERMİNALE, DİĞERLERİ KAPANMAYACAK)
komut6: rosrun odev2_map navigate_goal.py
BURADA odev2_map YERİNE KENDİ PAKETİNİZİ VE navigate_goal.py YERİNE DE KENDİ PYTHON KODUNUZUN ADINI YAZIN.



BU ŞEKİLDE ÖDEVİ TAMAMLAMIŞ OLDUK. ASLINDA ÇALIŞTIRMAK İÇİN 4 KOMUT KULLANDIK.
1) roscore
2) roslaunch turtlebot3_gazebo turtlebot3_house.launch
3) roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/home/zeynepsena/catkin_ws/src/ros_course_part2-master/src/topic03_map_navigation/tb3map/tb3_house_map_yaml
4) rosrun odev2_map navigate_goal.py



---------------------------------


