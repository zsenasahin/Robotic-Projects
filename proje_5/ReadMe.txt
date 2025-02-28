Proje: TurtleBot Otomatik ve Manuel Hareket Kontrolü

**Projenin Amacı**
Bu projede, TurtleBot'un hem belirlenen otomatik hareketleri gerçekleştirmesi hem de klavye kontrolü ile manuel olarak yönlendirilmesi sağlanmıştır. Ayrıca, TurtleBot'un hareket ettiği her adımda pozisyon bilgileri ekrana yazdırılmakta ve robotun bulunduğu ortamdaki sıcaklık verisi bir düğüm ile yayınlanmaktadır.

Adım-1
Öncelikle yeni bir paket oluşturuyoruz. Paketi catkin_ws workspace'si içerisinde src klasörünün içine oluşturuyoruz. Bu yola gitmek için şu kodu yazarız:
cd ~/catkin_ws/src

Daha sonra paket oluşturmak için şu kodu yazıyoruz:
catkin_create_pkg yeni_paket_adi std_msgs rospy roscpp

paketimiz oluştu. 


Adım-2
Daha sonra bu paketimizde launch ve scripts klasörlerimiz olacak.
Scripts klasöründe hareketi sağlayacak hareket.py, anlık olarak konum bilgisini takip edileceği yol.py ve hava apisinin çekileceği hava.py dosyalarımız olacak.

Launch klasöründe ise tüm bu işlemleri tek bir kod ile çalıştırmak için bir turtlebot_odev.launch dosyası oluşturduk. burada az önce bahsettiğim 3 kodu çalıştırmak için gereken node'leri yazdık.

*******************************************************************************

**hareket.py**

rospy: ROS (Robot Operating System) için Python arayüzüdür. ROS düğümlerini başlatmak, durdurmak ve arayüz sağlamak için kullanılır.

geometry_msgs.msg.Twist: Twist mesajı, TurtleBot'un lineer (doğrusal) ve açısal hız değerlerini içerir. linear.x ve angular.z parametrelerini kullanarak robotu hareket ettiririz.

sys, termios, tty: Bu modüller, klavye girişlerini doğrudan terminalden almak ve işlemleri kolaylaştırmak için kullanılır.

threading: Aynı anda birden fazla işlemi gerçekleştirmek için kullanılır.

get_key(): Terminalden tek bir tuş girişini okumak için kullanılan bir yardımcı fonksiyondur. termios ve tty modülleri kullanılarak klavyeden anlık tuş okuma sağlanır. get_key() fonksiyonu, w, a, s, d gibi tuşların algılanması için gereklidir.

hareket(): Ana fonksiyonumuz olan hareket() fonksiyonu, robotun önce belirlenen otomatik hareketleri gerçekleştirmesini, ardından manuel kontrol ile yönlendirilmesini sağlar.

rospy.init_node('hareket', anonymous=True): Bu, ROS ile bir düğüm (node) oluşturur ve düğümün adı 'hareket' olur. anonymous=True parametresi, aynı düğümün birden fazla kopyasının çalıştırılabilmesini sağlar.

Publisher (/cmd_vel): pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) ile bir Publisher oluşturulur. Bu publisher, Twist mesajları kullanarak /cmd_vel topic'ine hız bilgilerini gönderir. TurtleBot’un hareketini sağlamak için Twist mesajları kullanılır.

rate: rate = rospy.Rate(10) ifadesi, döngünün saniyede 10 kez çalışmasını sağlar.


İleri Gitme: linear.x değeri 0.1 olarak ayarlanır, yani robot ileriye doğru hareket eder. for döngüsü ile hareket süresi kontrol edilir. rate.sleep() fonksiyonu, hareketin belirli bir süre devam etmesini sağlar.

Dönme Hareketleri: angular.z değeri 0.5 (sola dönüş) veya -0.5 (sağa dönüş) olarak ayarlanır. Bu şekilde, robotun belirtilen açıda dönmesi sağlanır.

Durma ve Diğer Hareketler: Belirli bir mesafe veya açı geçildikten sonra linear.x ve angular.z sıfırlanarak robot durdurulur.

örneğin (ileri gitme kodu):
hareket.linear.x = 0.1
hareket.angular.z = 0.0
rospy.loginfo("İleri gidiyor...")
for _ in range(50):
    pub.publish(hareket)
    rate.sleep()


Hareket Komutlarının Gönderilmesi: Her tuş ile hareket komutları Twist mesajı kullanılarak pub.publish(hareket) komutu ile yayınlanır. Bu, robotun sürekli güncellenen hız bilgisi ile yönlendirilmesini sağlar.

Klavye Kontrolü: Bu döngü, w, a, s, d tuşları kullanılarak robotu manuel olarak kontrol eder. w ileri, s geri, a sola ve d sağa hareket için kullanılır. q tuşuna basıldığında ise döngüden çıkılarak program sonlanır.

Robotun Durdurulması: Program sona erdiğinde, linear.x ve angular.z sıfırlanarak robotun tüm hareketleri durdurulur. rospy.loginfo ile de programın sona erdiği kullanıcıya bildirilir.

*******************************************************************************

**yol.py**

Gerekli kütüphaneler:
import rospy
from nav_msgs.msg import Odometry

rospy: ROS (Robot Operating System) ile iletişim kurmak, düğüm başlatmak ve döngü çalıştırmak için kullanılan Python kütüphanesidir.

nav_msgs.msg.Odometry: TurtleBot'un pozisyonunu ve hızını sağlayan Odometry mesaj türünü içerir. Bu mesaj, robotun anlık pozisyon bilgisini (pose) almak için gereklidir.

YolTakibi sınıfı: TurtleBot’un pozisyon bilgisini dinlemek ve gidilen mesafeyi hesaplayıp yazdırmak için oluşturulmuştur.

rospy.init_node('yol', anonymous=True): Bu satır, ROS düğümünü 'yol' adıyla başlatır.

Subscriber (/odom): self.subscriber = rospy.Subscriber('/odom', Odometry, self.callback) satırı, TurtleBot’un /odom topic’ine abone olur ve her yeni Odometry mesajı geldiğinde callback fonksiyonunu çağırır. Bu topic, TurtleBot'un konum ve hız bilgisini içerir.

Pozisyon ve Mesafe Değişkenleri
prev_x ve prev_y, TurtleBot’un önceki x ve y pozisyonlarını kaydeder.

total_distance_x ve total_distance_y, TurtleBot’un toplamda x ve y eksenlerinde kat ettiği mesafeyi kaydeder.

is_moving, TurtleBot hareket halindeyken koordinatların ekrana yazdırılmasını kontrol eden bir bayraktır.

"callback" FONKSİYONU:
callback(msg): Odometry mesajlarıyla her güncellemede çalışır ve robotun mevcut pozisyonunu alır.

current_x ve current_y: msg.pose.pose.position.x ve msg.pose.pose.position.y bilgileri, robotun o anki x ve y koordinatlarını temsil eder.

MESAFE HESAPLAMA
distance_x ve distance_y, mevcut ve önceki pozisyon arasındaki fark olarak hesaplanır.
Bu fark, toplam mesafe değişkenlerine (total_distance_x ve total_distance_y) eklenir. Böylece, TurtleBot’un x ve y ekseninde toplam kat ettiği mesafe hesaplanmış olur.


display_distance(): is_moving bayrağı True olduğunda, toplam mesafeyi ekrana yazdırır. Mesafeler, rospy.loginfo ile log olarak ekrana yazdırılır ve iki ondalık basamakla gösterilir.

Koşul Kontrolü: is_moving bayrağı, robotun manuel kontrol durumunda olup olmadığını kontrol eder. Eğer robot manuel kontrol altındaysa mesafe bilgisi ekrana yazdırılır.


run(): Programın çalıştığı ana döngüdür.

rate = rospy.Rate(1): Döngü hızını ayarlar. Burada, döngü her saniyede bir (1 Hz) çalışır. display_distance fonksiyonu, belirli aralıklarla is_moving kontrolüne bağlı olarak bilgiyi ekrana yazdırır.

set_moving(moving): is_moving bayrağını güncellemek için kullanılan bir setter fonksiyonudur. Manuel kontrol sırasında bayrağı True olarak ayarlayarak mesafelerin yazdırılmasını sağlar.
********************************************************************************
hava.py

hava.py dosyası, Konya ilinin anlık hava sıcaklığını bir API üzerinden alıp, ROS ortamında yayınlamak için oluşturulmuş bir Python dosyasıdır. Bu dosyada, Konya'nın sıcaklık bilgisini bir ROS node'u aracılığıyla yayınlayan bir yapı bulunur.

GEREKLİ KÜTÜPHANELER

import rospy
import requests
from std_msgs.msg import String

AÇIKLAMASI:
rospy: ROS ile Python üzerinden iletişim kurmak için kullanılan temel kütüphanedir. Bu kütüphane, ROS düğümlerini başlatmayı, mesajları yayınlamayı ve dinlemeyi sağlar.
requests: HTTP istekleri yapmak için kullanılan bir Python kütüphanesidir. Bu kütüphane, OpenWeatherMap API’sinden veri çekmek amacıyla kullanılır.
std_msgs.msg.String: ROS sisteminde mesajlar, belirli bir türde olur. Burada String türü kullanılmıştır. Hava durumu bilgisini ROS sistemine string formatında iletmek için bu tür kullanılır.


getWeather() Fonksiyonu

api_key: OpenWeatherMap API’si için kullanıcıya özel bir API anahtarıdır. Bu anahtar, API ile iletişim kurmak ve veri almak için gereklidir. (Gerçek bir uygulamada bu anahtar gizli tutulmalı.)

url: OpenWeatherMap API’si için oluşturulmuş istek URL’sidir. Burada Konya'nın hava durumu bilgilerini almak için gerekli parametreler (q=Konya, appid=API_KEY, units=metric) eklenmiştir.

response.status_code == 200: Eğer API'den başarılı bir yanıt alınırsa (status code 200), hava durumu verisi çekilir. Bu durumda sıcaklık verisi data['main']['temp'] ile alınır.

publish_weather() Fonksiyonu

rospy.init_node('hava', anonymous=True): Bu satır, ROS düğümünü başlatır. 'hava' adında bir düğüm oluşturulur. anonymous=true parametresi, aynı ada sahip başka düğümler varsa bu düğümün adının benzersiz olmasını sağlar.

pub = rospy.Publisher('/konya_sicaklık', String, queue_size=10): konya_sicaklık adında bir ROS topic oluşturulur. bu topic üzeirnden hava durumu bilgisi yayınlanacaktır. String mesaj türü kullanılır ve queue_size = 10 ile mesaj kuyruğunda maksimum 10 mesaj saklanır.

rate = rospy.Rate(1): Bu satırda her saniye bir güncelleme yapılmasını sağlamak için bir rate belirlenir.

weather_info = get_Weather ile get_weather() fonksiyonu çağıralarak hava durumu bilgisi alınır.


****************************************************************************

**launch dosyası** (turtlebot_odev.launch)

<include>: Bu etiket, başka bir launch dosyasını içeri aktarmak için kullanılır. Burada, turtlebot3_gazebo paketinin içindeki turtlebot3_empty_world.launch dosyasını başlatıyoruz. Bu dosya, TurtleBot3 robotunu Gazebo simülasyon ortamında başlatmak için gereklidir ve "boş bir dünya" (empty world) olarak bilinen bir ortamda robotu konumlandırır. Bu sayede simülasyonda robot, hareket etmeye hazır bir şekilde çalışmaya başlar.

<node>: Bu etiket, ROS sisteminde bir node başlatmak için kullanılır. Burada, zeynepsena_sahin adlı paket içindeki hareket.py dosyasını bir node olarak çalıştırıyoruz. Bu node’un adı hareket olarak belirlenmiş ve çıktısı doğrudan ekranda görüntülenmesi için output="screen" parametresi eklenmiştir.

Burada aşağıdaki kod ile 3 kodumuzu(hareket, yol,hava) ortak bir şekilde çalıştırabiliyoruz.
  <!-- Turtlebot hareket node'u -->
  <node pkg="zeynepsena_sahin" type="hareket.py" name="hareket" output="screen"/>

  <!-- Pose bilgilerini dinleyip yol hesaplayan node -->
  <node pkg="zeynepsena_sahin" type="yol.py" name="yol" output="screen"/>

  <!-- Konya'nın sıcaklığını çeken hava node'u -->
  <node pkg="zeynepsena_sahin" type="hava.py" name="hava" output="screen"/>

************************************************************************************


Adım-3 (Çalıştırma)

Önceki projelerde genelde bir terminalde roscore yazıp rosu başlatıp ayrı bir terminalde programı çalıştırırdık. ama bu projede bu launch dosyası, birden fazla ROS node'unu aynı anda başlatabilmemizi sağlıyor. Bu dosya sayesinde, Gazebo simülasyonu başlatılır, robot hareket eder, yol bilgisi takip edilir ve hava durumu bilgisi alınarak ROS sisteminde yayımlanır.

Bu launch dosyasını çalıştırabilmemiz için tek yapmamız gereken terminali açmak ve şu kodu yazmak:
roslaunch paket_adiniz launch_dosyasi_adi.launch

bu kodu yazıp gönderdikten sonra otomatik olarak gazebo açılacak ve robot otomatik hareketine başlayacak. otomatik hareket bittikten sonra w a s d tuşları ile manuel olarak hareket ettirebilirsiniz!


























