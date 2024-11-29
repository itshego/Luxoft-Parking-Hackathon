from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QGridLayout, QLabel, QPushButton, QSpinBox, QHBoxLayout,
                            QFrame, QTextEdit)
from PyQt5.QtGui import QColor
import numpy as np
import sys
import time
from .parking_lot_view import ParkingLotView
from PyQt5.QtCore import Qt

class ParkingLotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Otopark Sistemi")
        self.setGeometry(100, 100, 800, 600)

        # Ana widget'ı oluştur
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout oluştur
        layout = QVBoxLayout(central_widget)
        
        # Boş bir ParkingLotView oluştur
        self.parking_lot_view = ParkingLotView()
        layout.addWidget(self.parking_lot_view)
        
        # Yol tarifi için metin alanı
        self.direction_text = QTextEdit()
        self.direction_text.setReadOnly(True)
        self.direction_text.setMaximumHeight(100)
        layout.addWidget(self.direction_text)
        
        # Pencereyi ortala
        self.center_on_screen()

    def center_on_screen(self):
        """Pencereyi ekranın ortasına konumlandır"""
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()
        
        # Pencereyi ekranın ortasına yerleştir
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def update_directions(self, path):
        """Yol tarifini güncelle"""
        if not path:
            self.direction_text.setText("Uygun park yeri bulunamadı!")
            return
            
        directions = []
        for i in range(len(path) - 1):
            current = path[i]
            next_pos = path[i + 1]
            
            # Yön belirleme
            dy = next_pos[0] - current[0]
            dx = next_pos[1] - current[1]
            
            if dy == 1:
                directions.append("1 birim güneye git")
            elif dy == -1:
                directions.append("1 birim kuzeye git")
            elif dx == 1:
                directions.append("1 birim doğuya git")
            elif dx == -1:
                directions.append("1 birim batıya git")
        
        # Son adımda park etme talimatı
        directions.append("Park et!")
        
        # Yönergeleri metin kutusuna ekle
        self.direction_text.setText("\n".join(directions))

def visualize_parking_lot_qt(rows=20, cols=40):
    """Park alanı görselleştirme fonksiyonu"""
    app = QApplication(sys.argv)
    
    # İlk pencereyi oluştur
    window = ParkingLotWindow(rows, cols)
    window.show()
    window.create_parking_lot()  # İlk park alanını oluştur
    
    return app.exec() 