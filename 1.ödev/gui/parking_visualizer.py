from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QGridLayout, QLabel, QPushButton, QSpinBox, QHBoxLayout,
                            QFrame)
from PyQt5.QtGui import QColor
import numpy as np
import sys
import time
from .parking_lot_view import ParkingLotView

class ParkingLotWindow(QMainWindow):
    def __init__(self, rows=20, cols=40):
        super().__init__()
        self.setWindowTitle('Park Alanı Görüntüleyici')
        self.setMinimumSize(800, 600)

        self.rows = rows
        self.cols = cols
        self.occupancy_rate = 0.7

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        main_layout.addLayout(self._create_control_panel())

        empty_lot = np.zeros((self.rows, self.cols), dtype=np.int8)
        self.parking_widget = ParkingLotView(empty_lot, (0,0), None)
        main_layout.addWidget(self.parking_widget)
        
        bottom_layout = QHBoxLayout()

        bottom_layout.addWidget(self._create_legend())
        
        main_layout.addLayout(bottom_layout)
        
        # İlk performans ölçümü
        self.update_performance_stats()
#region Panels
    def _create_control_panel(self):
        """Kontrol panelini oluştur"""
        control_panel = QHBoxLayout()
        control_panel.setSpacing(15)
        
        # Matris boyutları için spinbox'lar
        size_layout = QHBoxLayout()
        size_layout.setSpacing(5)
        size_layout.addWidget(QLabel("Boyut:"))
        
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 512)
        self.rows_spin.setValue(self.rows)
        size_layout.addWidget(self.rows_spin)
        
        size_layout.addWidget(QLabel("x"))
        
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 512)
        self.cols_spin.setValue(self.cols)
        size_layout.addWidget(self.cols_spin)
        
        control_panel.addLayout(size_layout)
        
        # Doluluk oranı ayarı
        rate_layout = QHBoxLayout()
        rate_label = QLabel("Doluluk Oranı:")
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(0, 100)
        self.rate_spin.setSuffix("%")
        self.rate_spin.setValue(int(self.occupancy_rate * 100))
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_spin)
        control_panel.addLayout(rate_layout)
        
        # Yeniden oluştur butonu
        self.recreate_button = QPushButton("Yeniden Oluştur")
        self.recreate_button.clicked.connect(self.create_parking_lot)
        control_panel.addWidget(self.recreate_button)
        
        # Performans göstergesi
        self.perf_label = QLabel()
        control_panel.addWidget(self.perf_label)
        
        return control_panel

    def _create_legend(self):
        """Lejant frame'ini oluştur"""
        legend_frame = QFrame()
        legend_frame.setFrameStyle(QFrame.StyledPanel)
        legend_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        legend_layout = QGridLayout(legend_frame)
        legend_items = [
            ('Boş Park Yeri', QColor(0, 255, 0, 180)),
            ('Dolu Park Yeri', QColor(255, 0, 0, 180)),
            ('En Uygun Park Yeri', QColor(0, 0, 255, 180)),
            ('Başlangıç Noktası', QColor(0, 0, 0))
        ]
        
        # Sol taraf: Renkli kutular ve açıklamaları
        for i, (text, color) in enumerate(legend_items):
            color_box = QWidget()
            color_box.setFixedSize(30, 30)
            color_box.setStyleSheet(f"""
                background-color: rgba({color.red()}, {color.green()}, 
                                     {color.blue()}, {color.alpha()});
                border: 1px solid gray;
                border-radius: 5px;
            """)
            legend_layout.addWidget(color_box, i, 0)
            legend_layout.addWidget(QLabel(text), i, 1)
        
        # Dikey ayırıcı çizgi
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)
        legend_layout.addWidget(vline, 0, 2, 4, 1)  # 4 satır boyunca uzanan çizgi
        
        # Sağ taraf: Bilgi etiketleri
        self.info_labels = {}
        
        # Zoom bilgisi
        self.info_labels['zoom'] = QLabel("Zoom: 1.0x")
        legend_layout.addWidget(self.info_labels['zoom'], 0, 3)
        
        # Matris boyutu
        self.info_labels['size'] = QLabel(f"Boyut: {self.rows}x{self.cols}")
        legend_layout.addWidget(self.info_labels['size'], 1, 3)
        
        # Başlangıç noktası
        self.info_labels['start'] = QLabel(f"Başlangıç: (0, 0)")
        legend_layout.addWidget(self.info_labels['start'], 2, 3)
        
        # Hedef noktası ve mesafe
        self.info_labels['target'] = QLabel("En uygun park yeri: Bulunamadı")
        legend_layout.addWidget(self.info_labels['target'], 3, 3)
        
        return legend_frame
#endregion

#region Update Functions
    def update_performance_stats(self, generation_time=0.00):
        """Performans istatistiklerini güncelle"""
        stats = []
        stats.append(f"Oluşturma Süresi: {generation_time:.3f}s")
        stats.append(f"Matris Boyutu: {self.rows}x{self.cols}")
        stats.append(f"Doluluk Oranı: %{self.occupancy_rate*100:.1f}")
        
        self.perf_label.setText(" | ".join(stats))

    def update_info_labels(self):
        """Bilgi etiketlerini güncelle"""
        # Zoom bilgisi
        self.info_labels['zoom'].setText(f"Zoom: {self.parking_widget.scale_factor:.1f}x")
        
        # Matris boyutu
        self.info_labels['size'].setText(f"Boyut: {self.rows}x{self.cols}")
        
        # Başlangıç noktası
        start = self.parking_widget.start_pos
        self.info_labels['start'].setText(f"Başlangıç: ({start[0]}, {start[1]})")
        
        # Hedef noktası ve mesafe
        best_spot = self.parking_widget.best_spot
        if best_spot is not None:
            distance = abs(best_spot[0] - start[0]) + abs(best_spot[1] - start[1])
            self.info_labels['target'].setText(
                f"En uygun park yeri: ({best_spot[0]}, {best_spot[1]}), Mesafe: {distance} birim"
            )
        else:
            self.info_labels['target'].setText("En uygun park yeri: Bulunamadı")
#endregion

#region Create
    def create_parking_lot(self):
        """Park alanını oluştur"""
        start_time = time.perf_counter()
        
        # Yeni boyutları al
        self.rows = self.rows_spin.value()
        self.cols = self.cols_spin.value()
        
        # Toplam hücre sayısı
        total_cells = self.rows * self.cols
        # İstenen dolu hücre sayısı
        occupancy = self.rate_spin.value() / 100
        desired_occupied = int(total_cells * occupancy)
        
        # Önce tüm park yerlerini dolu yap
        parking_lot = np.ones((self.rows, self.cols), dtype=np.int8)
        
        # Rastgele seçilen konumları boşalt
        empty_count = total_cells - desired_occupied
        empty_positions = np.random.choice(total_cells, empty_count, replace=False)
        parking_lot.flat[empty_positions] = 0
        
        # Başlangıç noktası seç
        start_pos = (np.random.randint(0, self.rows), 
                    np.random.randint(0, self.cols))
        parking_lot[start_pos] = 1  # Başlangıç noktasını işaretle
        
        # En yakın boş yeri bul
        empty_spots = np.where(parking_lot == 0)
        if len(empty_spots[0]) == 0:
            best_spot = None
        else:
            distances = (np.abs(empty_spots[0] - start_pos[0]) + 
                        np.abs(empty_spots[1] - start_pos[1]))
            min_idx = np.argmin(distances)
            best_spot = (empty_spots[0][min_idx], empty_spots[1][min_idx])
        
        # Widget'ı güncelle
        self.parking_widget.update_data(parking_lot, start_pos, best_spot)
        
        # Performans istatistiklerini güncelle
        end_time = time.perf_counter()
        self.update_performance_stats(end_time - start_time)


def visualize_parking_lot_qt(rows=20, cols=40):
    """Park alanı görselleştirme fonksiyonu"""
    app = QApplication(sys.argv)
    
    # İlk pencereyi oluştur
    window = ParkingLotWindow(rows, cols)
    window.show()
    window.create_parking_lot()  # İlk park alanını oluştur
    
    return app.exec() 
