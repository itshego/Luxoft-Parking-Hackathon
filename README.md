# Luxoft-Parking-Hackathon

# 1. Proje Açıklaması

Bu proje, verilen boyutlarda rastgele bir park alanı oluşturan ve en yakın boş park yerini bulan bir görsel uygulamadır.

## Özellikler

- Özelleştirilebilir matris boyutu (1x1 ile 512x512 arası)
- Ayarlanabilir doluluk oranı (%0-%100)
- Rastgele başlangıç noktası belirleme
- Manhattan mesafesine göre en yakın boş park yerini bulma
- Zoom ve pan özellikleri
- PyQt5 QGraphicsView kullanılarak grafik kartı ile görselleştirme
- Performans ölçümü

## Kullanım

1. Matris boyutunu "Boyut" spinbox'larından ayarlayın
2. Doluluk oranını "Doluluk Oranı" spinbox'ından ayarlayın
3. "Yeniden Oluştur" butonuna tıklayarak yeni bir park alanı oluşturun
4. Mouse tekerleği ile zoom yapın
5. Sağ tıklayıp sürükleyerek pan yapın

## Renkler

- 🟩 Yeşil: Boş park yeri
- 🟥 Kırmızı: Dolu park yeri
- 🟦 Mavi: En yakın boş park yeri
- ⬛ Siyah: Başlangıç noktası

- Matris oluşturma ve en yakın nokta hesaplama NumPy ile optimize edilmiştir
- GPU hızlandırmalı çizim için QGraphicsView kullanılmıştır
- Minimum çizim çağrısı için optimizasyon yapılmıştır
![v1](https://github.com/user-attachments/assets/65026dd9-a47c-4036-90d4-f6b6a04d8fac)


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
