***PROJE ÖZETİ***

Bu proje, ROS ortamında turtlesim paketini kullanarak sanal bir robotun ızgara düzeninde hareket etmesini simüle eder. Proje, robotun hareket ve dönüş kontrollerini uygulayarak ızgara boyunca doğrusal ve hizalı bir şekilde hareket etmesini sağlar.

*********************************************************
***Nasıl Çalışıyor?***

Projenin ana fonksiyonu, kaplumbağanın kare şeklinde bir ızgara içinde hareket etmesini sağlamaktır. İşte projenin temel işlevleri:

Kaplumbağayı Hareket Ettirme (move fonksiyonu): Kaplumbağa belirlenen bir mesafe boyunca düz bir çizgide ilerler. Hızı ve yönü (ileri veya geri) kontrol edilir ve robotun hedeflenen mesafeye ulaşıp ulaşmadığı sürekli kontrol edilir.
move kodu: def move(publisher, speed, distance, is_forward):

Kaplumbağayı Döndürme (rotate fonksiyonu): Kaplumbağa yerinde sabit bir açıyla (örn. 90 derece) saat yönünde ya da tersine döner. Bu işlem, her hareketten sonra robotun doğru hizalanarak bir sonraki harekete geçmesini sağlar.
rotate kodu: def rotate(publisher, angular_speed_degree, relative_angle_degree, clockwise):
    
Hedefe Gitme (go_to_goal fonksiyonu): Kaplumbağa, verilen bir (x, y) koordinatına doğru hareket eder.

Izgara Deseninde Hareket Etme (gridClean fonksiyonu): Projenin ana işlevi budur. Kaplumbağayı ızgara temizleme işlemi boyunca hareket ettirir. Döngü kullanarak robot ileri hareket eder, döner ve tekrar hareket eder, bu şekilde bir ızgara düzeni oluşturur.

gridClean kodu: def gridClean(publisher):
   

*********************************************************
***Nasıl Çalıştırılır?***

Öncelikle terminali açıp roscore yazıyoruz ve rosu başlatıyoruz. 
Daha sonra terminali kapatmadan yeni bir terminal açıyoruz ve turtlesim başlatıyoruz. Turtlesim başlatmak için aşağıdaki kodu yazıyoruz:
rosrun turtlesim turtlesim_node
bu kodu yazdıktan sonra ekranda robotumuz çıkacaktır.

Daha sonra turtlesim için yaptığımız paketin içinde ki cleaner kodunu çalıştırıyoruz. örneğin benim paketimin adı ros_tutorials ve cleaner kodumun adı tosbik_cleaner.py ve aşağıdaki kodu yazıyorum.
rosrun ros_tutorials tosbik_cleaner.py
bu kodu yazdıktan sonra robotumuz harekete başlayacaktır

