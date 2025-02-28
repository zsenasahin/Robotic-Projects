# ROS ile Robot Simülasyonu (Publisher ve Subscriber)

Bu proje, ROS (Robot Operating System) kullanarak hareket eden bir robotu simüle eder. Robot, başlangıç koordinatı olan (1, 1, 1) noktasından harekete başlar ve rastgele bir şekilde belirlenen hedefe doğru hareket eder. Simülasyon iki ana bileşenden oluşur:
- **Publisher** düğümü: Robotun koordinatlarını belirli aralıklarla yayar.
- **Subscriber** düğümü: Robotun koordinatlarını dinleyip, robotun hedefe ulaşıp ulaşmadığını kontrol eder.

--Proje Özeti--

- Publisher Düğümü: Bu düğüm, robotun mevcut koordinatlarını (`robot_coordinates_topic` adlı bir konuya) saniyede bir yazar. X ve Y koordinatları rastgele güncellenir, Z ise sabit `1` olarak tutulur. Yayınlanan mesajlar şunları içerir:
  - `ID`: Robotun kimliği (sabit olarak `1`).
  - `Name`: Robotun adı (`robot_01`).
  - `X`: Rastgele güncellenen X koordinatı (başlangıçta 1).
  - `Y`: Rastgele güncellenen Y koordinatı (başlangıçta 1).
  - `Z`: Sabit Z koordinatı (1).
  - Yayınlanan her mesajın zamanı da terminalde yazdırılır.

- Subscriber Düğümü: Bu düğüm, robotun koordinatlarını dinler. Gelen her mesajda:
  - Koordinatlar ve zaman terminale yazdırılır.
  - Robotun hedef koordinatlara (5, 5, 5) ulaşıp ulaşmadığını kontrol eder. Eğer hedefe ulaşıldıysa, "Robot hedefe ulaştı!" mesajı yazdırılır.

--Kullanım--

1. Gerekli Adımlar
Proje ROS ortamında çalışacak şekilde hazırlanmıştır. Başlamadan önce ROS'u ve Python ROS kütüphanelerini kurmamız gerekir.
Daha sonra terminal açıp roscore diyoruz ve rosu başlatıyoruz. 

2. Publisher Düğümünü Çalıştırmak
Publisher düğümünü başlatmak için aşağıdaki komutu terminalde çalıştırın:

rosrun <paket_adı> publisher_robot.py

Subscriber düğümünü başlatmak için yeni bir terminal açıp aşağıdaki kodu çalıştırın.

rosrun <paket_adı> subscriber_robot.py

Bu komutlardan sonra iki ekranda da robotumuz harekete geçecektir.

Hedefe ulaşmadan durdurmak istediğimizde ctrl+c ile durdururuz
