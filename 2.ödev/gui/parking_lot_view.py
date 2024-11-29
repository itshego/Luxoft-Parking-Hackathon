from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QPainter
import numpy as np

class ParkingLotView(QGraphicsView):
    def __init__(self, parking_lot=None, start_pos=None, best_spot=None):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Başlangıç değerleri
        self.parking_lot = parking_lot
        self.start_pos = start_pos
        self.best_spot = best_spot
        
        # Görünüm ayarları
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        if parking_lot is not None:
            self.draw_parking_lot()
        
    def update_data(self, parking_lot, start_pos, best_spot):
        """Verileri güncelle ve yeniden çiz"""
        self.parking_lot = parking_lot
        self.start_pos = start_pos
        self.best_spot = best_spot
        self.draw_parking_lot()
        
    def draw_parking_lot(self):
        """Otoparkı çiz"""
        if self.parking_lot is None:
            return
            
        self.scene.clear()
        rows, cols = self.parking_lot.shape
        cell_size = min(self.width() / cols, self.height() / rows)
        
        for i in range(rows):
            for j in range(cols):
                x = j * cell_size
                y = i * cell_size
                
                # Hücre rengini belirle
                if (i, j) == self.start_pos:
                    color = QColor(0, 0, 0)  # Başlangıç noktası - Siyah
                elif (i, j) == self.best_spot:
                    color = QColor(0, 0, 255)  # En iyi park yeri - Mavi
                elif self.parking_lot[i, j] == 2:
                    color = QColor(128, 128, 128)  # Yol - Gri
                elif self.parking_lot[i, j] == 1:
                    color = QColor(255, 0, 0)  # Dolu park yeri - Kırmızı
                else:
                    color = QColor(0, 255, 0)  # Boş park yeri - Yeşil
                
                # Hücreyi çiz
                self.scene.addRect(x, y, cell_size, cell_size, 
                                 QPen(Qt.black), 
                                 QBrush(color))
        
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        
    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde görünümü güncelle"""
        super().resizeEvent(event)
        if self.parking_lot is not None:
            self.draw_parking_lot()
