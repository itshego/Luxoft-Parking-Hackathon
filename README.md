# Luxoft-Parking-Hackathon




## 2. Proje Açıklaması
Bu proje, otomatik park yeri bulma ve yönlendirme sistemi sunan bir Python uygulamasıdır. Ağırlıklı graf algoritmaları kullanarak, araç sürücülerini en uygun boş park yerine yönlendirir.

## Özellikler
- Otomatik otopark düzeni oluşturma
- En kısa yol algoritması (Dijkstra) ile optimal park yeri bulma
- Görsel arayüz ile otopark durumunu gösterme
- Adım adım yönlendirme talimatları
- Özelleştirilebilir otopark boyutu ve doluluk oranı
- PyQt5 QGraphicsView kullanılarak grafik kartı ile görselleştirme (1000x1000 matris bile yapılsa bilgisayar cık etmeyecektir, sadece üretirken biraz yavaş kalabilir o kadar rect'i nested loop'la eklemek biraz zor olur, vektörel yapabilirdim ama zamanı iyi kontrol edemedim)


1. Program başlatıldığında otomatik olarak bir otopark düzeni oluşturulur
2. Renk kodları:
   - 🟢 Yeşil: Boş park yerleri
   - 🔴 Kırmızı: Dolu park yerleri
   - ⚫ Gri: Yollar
   - ⚫ Siyah: Başlangıç noktası
   - 🔵 Mavi: Bulunan en uygun park yeri
3. Alt kısımda adım adım yönlendirme talimatları görüntülenir

![v2](https://github.com/user-attachments/assets/7ec4d8e5-d457-4063-bd13-d50577f8b6ad)
