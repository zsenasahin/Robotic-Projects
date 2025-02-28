Bu proje, ROS (Robot Operating System) kullanarak basit bir "Dikdörtgenin Alanını Hesaplama" servisini içermektedir. Proje, dikdörtgenin genişliği ve yüksekliği alındığında, alanını hesaplayarak sonuç döndüren bir ROS servisi sağlar. Ayrıca bir istemci kodu, genişlik ve yükseklik verilerini servise gönderir ve sonuç olarak alanı geri alır.

***KURULUM***

1)Ros yüklü değilse ros noetic yükleyin.

2)Catkin Workspace oluşturun:
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make

3)Servis mesajlarını tanımlayın. srv klasörünün içine girip oraya .srv uzantılı dosyayı oluşturun ve içine şunları yazın:
int32 width
int32 height
---
int32 area
Eğer değişkenleriniz float ise int yerine float yazın!!

4)CMakeLists.txt güncelleyin. service kısmına kendi srv dosyasınızın ismini de ekleyin.

5) Projeyi derleyin.
cd ~/catkin_ws
catkin_make

***************************

Proje iki ana parçadan oluşuyor. server ve client.

Dikdörtgenin alanını hesaplamak için öncelikle server çalıştırın.
rosrun <paket_adı> multipl_server.py

multipl_server.py kısmına kendi server dosyasınızın adını girin.

daha sonra client çalıştırın ve genişlikle yüksekliği girin.

rosrun <paket_adı> multipl_client.py 5 10

Terminalde sonucu göreceksiniz.

