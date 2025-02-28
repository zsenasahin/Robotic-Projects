Final Projesi

*** PROJENİN AMACI ***
Bu projede gazebo da turtlebot_house dünyasında robotun herhangi bir noktadan başlatıp ilk olarak kendisine en yakın olan duvarı bulmasını ve oraya gitmesini sağlıyor. Robot en yakın duvara ulaştıktan sonra ise harekete ordan başlayarak tüm kenarları dolaşıp tekrar başladığı konuma geliyor. Bu hareket bittiğinde hareket sayesinde açılan harita scripts klasörünün içine kaydediliyor. Daha sonra ise bu harita kullanılarak robotun son geldiği noktadan başlayarak tüm odayı tarayacak şekilde sol duvardan sağ duvara doğru bir aşağı bir yukarı şeklinde tüm alanı geziyor. 


*** PROJENİN ÇALIŞTIRILMASI ***

Adım 1: İlk olarak terminali açıp gazebo ortamını açıyoruz. bunun için terminale şu komutu yazıyoruz:
komut1: roslaunch turtlebot3_gazebo turtlebot3_house.launch
bu sayede house dünyasında gazebo ortamımızı açmış olduk.

Burada şöyle bir düzenleme yapıldı: robotun daha rahat hareket etmesi ve fiziksel engellere takılmaması için house dünyasının model.sdf dosyasında düzenlemeler yaptım.
ilk olarak odadaki çöp kutusunu tamamen sildim. Daha sonra odanın bir duvarında kapı olduğu için o kapıyı kaldırıp yerine düz duvar ekledim.
Son olarak da house dünyasının launch dosyasında robotun başlangıç konumunu değiştirerek düzenleme yaptığım odanın içinde başlamasını sağladım.

Adım 2: Terminale aşağıdaki komutu yazarak daha sonralarında kullanacağımız harita için slam başlattık. Detaylı açıklamalarını aşağıda anlatacağım.
komut2: roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping

Şimdi hareketlere başlıyoruz. ilk olarak en yakın duvara gitmesi için scripts klasörümüzde bulunan robot_control.py kodunu çalıştıracağız:
komut3: rosrun final_odevi robot_control.py 
final_odevi benim paketimin adı oraya kendi paketinizi yazabilirsiniz..

bu kod çalıştığında robot etrafını 360 derece tarayacak ve kendisine en yakın olan duvarı bulup oraya gidecek.

ikinci olarak az önce geldiği noktadan başlayarak tüm kenarları gezmesini istiyorduk. bunun için terminale şu komutu yazıyoruz:
komut4: rosrun final_odevi robot_control2.py

robot_control2 kodu sayesinde robot en son hangi yönde durduysa o yönden başlayarak tüm duvarları takip etmesini sağlıyoruz.


son olarak da temizlik işlemini yapıyoruz. burada robot başladığı noktadan ilk önce düz şekilde gidiyor ve herhangi bir engelle karşılaştığında sağa dönüp biraz ilerliyor ve tekrar sağa dönüp aşağı gidiyor, sonra sola dönüp biraz ilerliyor ve tekrar sola dönüp düz ilerliyor, bu şekilde tüm alan bitene kadar bu harekete devam ediyor... 

Bunun için komut: 
komut5: rosrun final_odevi robot_control3.py

Eğer burada hareketi daha rahat gözlemlemek isterseniz komut4 bittikten sonra gazebo da reset world diyip robotu sol alt köşeye koyup komut5i çalıştırabilirsiniz. hareket daha net şekilde gözlemlenecektir.


----------------------------------------------------------------------------------------------

*** PROJE KODLARININ AÇIKLANMASI ***

robot_control.py : EN YAKIN DUVARA GİTME

LaserScan ve Twist: Sensör ve hareket komutları için ROS mesaj tipleri.

Publisher (self.vel_pub): Robotun hız komutlarını (Twist mesajları) yayınlar.

Subscriber (self.scan_sub): Robotun lazer tarama verilerini (LaserScan mesajları) dinler ve işlemek için laser_callback metodunu kullanır.

self.safe_distance: Robotun güvenli mesafede durması için hedef mesafeyi tanımlar.

self.min_distance ve self.min_angle: En yakın duvarın mesafesini ve yönünü depolamak için kullanılır.

--Lazer Verilerini Dinleme--

def laser_callback(self, msg):
    self.laser_data = msg.ranges
    
Yukarıdaki kod da amaç: Lazer tarayıcının (LiDAR) gönderdiği mesafeleri (ranges) alır ve self.laser_data değişkenine kaydeder.

ranges: 360 derecelik bir alandaki engellere olan mesafeleri içeren bir liste.


--Robotu döndürme ve durdurma--
def rotate(self, angular_speed):
    vel_msg = Twist()
    vel_msg.angular.z = angular_speed
    self.vel_pub.publish(vel_msg)

Robotu belirli bir açısal hızla (angular_speed) döndürmek için cmd_vel kanalına bir hız mesajı (Twist) gönderir.


def stop(self):
    vel_msg = Twist()
    self.vel_pub.publish(vel_msg)

Robotu durdurmak için bir Twist mesajı yayınlanır (linear ve angular hız sıfırdır).


--En yakın duvara doğru ilerleme--

def move_towards_wall(self):
    rospy.loginfo("Moving towards the nearest wall")
    vel_msg = Twist()
    vel_msg.linear.x = 0.2

Amaç: Robot, güvenli mesafeye ulaşana kadar ileri hareket eder.
Lazer verilerinden ön taraftaki en küçük mesafeyi kontrol eder:
min_distance_in_front = min(self.laser_data[0:30] + self.laser_data[-30:])

Eğer güvenli mesafeden uzaktaysa (min_distance_in_front > self.safe_distance), robot hareket etmeye devam eder.
Güvenli mesafeye ulaştığında durur ve bir bilgi mesajı loglanır.


--360 derece dönme ve tarama--

self.rotate(math.pi / 18): 10 derece dönüş için gerekli açısal hız kullanılır.

if distance < self.min_distance and distance > 0.5:
    self.min_distance = distance
    self.min_angle = i

Lazer verilerinde, 0.5 metreden uzak ve en kısa mesafeyi bulur:


target_angle = self.min_angle * math.pi / 180
vel_msg.angular.z = 0.5 if target_angle > 0 else -0.5

Hedef Açıyı Hesaplama: En yakın duvarın bulunduğu açıyı radyana çevirir.
Dönme Süresi: Robotun bu açıya dönmesi için gereken süre hesaplanır:
rotation_time = abs(target_angle) / 0.5


---------------------------------------

robot_control2.py : KENARLARI DOLAŞMA

os: Harita kaydetme işlemi için sistem komutlarını çalıştırır.
LaserScan ve Twist: Sensör ve hareket komutları için ROS mesaj tipleri.

ObstacleAvoidance Sınıfı

Düğümü başlatır: rospy.init_node('obstacle_avoidance', anonymous=True)
Publisher ve Subscriber:
/cmd_vel: Robotun hareket komutlarını yayınlamak için.
/scan: LIDAR'dan gelen mesafe verilerini almak için.
Parametreler:
safe_distance: Engel algılama için güvenli mesafe, 0.5 metre olarak ayarlanmış.
rate: İşlemlerin saniyede 10 kez yapılmasını sağlar (10 Hz).
map_saved: Haritanın yalnızca bir kez kaydedildiğini kontrol eder.
start_time: Robotun çalışmaya başladığı zamanı kaydeder.

scan_callback Fonksiyonu: LIDAR Verilerini İşler
front: Ön taraftaki en yakın mesafeyi kontrol eder (ilk ve son 30 derece).
left: Sol taraf mesafesi (60-120 derece arası).
right: Sağ taraf mesafesi (240-300 derece arası).

Eğer mesafe safe_distance (0.5 metre) altındaysa:
İleri hareket durdurulur.
Sağ ya da sola dönülür. Dönüş yönü, engelin hangi tarafta daha uzak olduğuna göre belirlenir.

Engel yoksa robot ileri hareket eder.

save_map Fonksiyonu: Harita daha önce kaydedildiyse işlem yapılmaz (if not self.map_saved).
Sistemde rosrun map_server map_saver -f ~/catkin_ws/src/final_odevi/src/map komutunu çalıştırır.
Harita, belirtilen dizine kaydedilir.
map_saved: Haritanın kaydedildiğini işaretler.

--------------------------------------

robot_control3.py : TEMİZLEME İŞLEMİ (IZGARA ŞEKLİ)

/cmd_vel: Robotun hız komutlarını (Twist mesajları) gönderir.
/scan: LIDAR'dan gelen mesafe bilgilerini alır.
/odom: Robotun pozisyon ve yönelim bilgilerini alır.

Robotun pozisyonu (x, y) ve yönü (theta) self.position sözlüğünde tutulur.
self.scan_data: LIDAR taramalarından alınan mesafe verilerini saklar.

linear_speed: Doğrusal hareket için hız (0.15 m/s).
angular_speed: Dönüş hızı (0.5 rad/s).

odom_callback: Robotun pozisyon ve yönelim bilgilerini /odom mesajlarından günceller.

laser_callback: Robotun etrafındaki engelleri algılamak için /scan mesajlarını işler.

check_obstacle: LIDAR verilerini kullanarak robotun önündeki (-30° ile +30° arası) mesafeleri kontrol eder.
Eğer en kısa mesafe güvenli mesafeden küçükse (stopping_distance, 0.4 metre), engel algılanmış sayılır.

move_forward: Robotu ileri hareket ettirir.

turn(target_angle): Robotu belirtilen bir hedef açıya çevirir. Robotun mevcut açısıyla hedef açı arasındaki fark hesaplanır ve robot, açı farkı belirli bir eşik değerden büyük olduğu sürece döner.

execute_movement fonksiyonu, robotun hareket durumlarını yönetir. Hareket modelindeki ana durumlar:
MOVE_FORWARD: 
   Robot ileri hareket eder.
   Eğer bir engelle karşılaşılırsa:
       Durur.
       TURN_RIGHT durumuna geçer.
       
TURN_RIGHT:
   Robot, 90° sağa döner.
   Dönüş tamamlandığında:
       MOVE_SIDE durumuna geçer.
       
MOVE_SIDE:
   Robot yan taraf boyunca hareket eder.
   Belirlenen mesafeye ulaştığında veya engel algıladığında:       
       TURN_RIGHT_1 durumuna geçer.
     
TURN_RIGHT_1:
   Robot, tekrar 90° sağa döner.
   Dönüş tamamlandığında:  
       MOVE_DOWN durumuna geçer.
       
MOVE_DOWN:
   Robot aşağı doğru hareket eder.
   Engel algılanırsa veya hedefe ulaşırsa:
       TURN_LEFT durumuna geçer.
       
TURN_LEFT      
   Robot 90° sola döner ve MOVE_SIDE_1 durumuna geçer.
   
MOVE_SIDE_1 ve TURN_LEFT_1
    MOVE_SIDE_1: Yan hareketin bir diğer versiyonu.
    TURN_LEFT_1: Sol dönüş işlemi.   

Durumların sıralı bir şekilde ilerlemesi, robotun ızgarayı taramasını ve engellerle karşılaşmadan hareket etmesini sağlar.

---------------

proje bu şekildedir. toplam 5 adet komut ile tüm projeyi gerçekleştiririz.











