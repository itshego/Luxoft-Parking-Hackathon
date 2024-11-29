from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
import numpy as np

class ParkingLotView(QGraphicsView):
    def __init__(self, parking_lot, start_pos, best_spot, parent=None):
        super().__init__(parent)
        
        self.parking_lot = parking_lot
        self.start_pos = start_pos
        self.best_spot = best_spot

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.NoFrame)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)      
        self.setMinimumSize(400, 200)
        self.setMouseTracking(True)
        
        self.scale_factor = 1.0
        self.is_panning = False
        self.last_mouse_pos = None
        
        self.draw_parking_lot()

    def draw_parking_lot(self):
        self.scene.clear()
        rows, cols = self.parking_lot.shape
        
        # Hücre boyutunu hesapla
        cell_size = min(self.width() / cols, self.height() / rows)
        
        # Toplam grid boyutunu hesapla
        total_width = cols * cell_size
        total_height = rows * cell_size
        
        # Scene boyutunu ayarla (grid'in 3 katı)
        scene_width = total_width * 3
        scene_height = total_height * 3
        
        # Scene'i merkeze hizalı olarak ayarla
        self.scene.setSceneRect(-scene_width/2, -scene_height/2, scene_width, scene_height)
        
        # Grid'i merkeze yerleştir
        start_x = -total_width/2
        start_y = -total_height/2
        
        # Koordinatları hesapla
        x_coords = start_x + np.arange(cols) * cell_size
        y_coords = start_y + np.arange(rows)[:, np.newaxis] * cell_size
        
        # Renk matrisini oluştur
        color_matrix = np.full(self.parking_lot.shape, QColor(0, 255, 0, 180))
        color_matrix[self.parking_lot == 1] = QColor(255, 0, 0, 180)
        color_matrix[self.start_pos] = QColor(255, 255, 255)
        if self.best_spot:
            color_matrix[self.best_spot] = QColor(0, 0, 255, 180)
        thin_pen = QPen(Qt.gray)
        thin_pen.setWidth(0)  # En ince çizgi kalınlığı

        # Dikdörtgenleri çiz
        for i in range(rows):
            for j in range(cols):
                self.scene.addRect(
                    x_coords[j], 
                    y_coords[i][0], 
                    cell_size, 
                    cell_size,
                    thin_pen,
                    QBrush(color_matrix[i, j])
                )
        
        # Görünümü merkeze ayarla
        self.centerOn(0, 0)
#region Mouse Events
    def wheelEvent(self, event):
        """Mouse wheel eventi ile zoom kontrolü"""
        if event.angleDelta().y() > 0:
            factor = 1.15
        else:
            factor = 1 / 1.15
            
        self.scale_factor *= factor
        self.scale_factor = max(0.1, min(100.0, self.scale_factor))
        
        self.scale(factor, factor)
        
        if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'update_info_labels'):
            self.parent().parent().update_info_labels()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_panning = False
            self.setCursor(Qt.ArrowCursor)
            
    def mouseMoveEvent(self, event):
        if self.is_panning:
            delta = event.pos() - self.last_mouse_pos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y())
            self.last_mouse_pos = event.pos()
#endregion

#region Update
    def update_data(self, parking_lot, start_pos, best_spot):
        """Verileri güncelle ve yeniden çiz"""
        self.parking_lot = parking_lot
        self.start_pos = start_pos
        self.best_spot = best_spot
        self.draw_parking_lot()
        if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'update_info_labels'):
            self.parent().parent().update_info_labels()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.draw_parking_lot() 
#endregion
