from gui.parking_visualizer import ParkingLotWindow
from parking_algorithm import ParkingAlgorithm
import numpy as np
from PyQt5.QtWidgets import QApplication
import sys
import random

def create_parking_lot(rows=9, cols=9, occupancy_rate=0.3):
    """
    Otomatik otopark matrisi oluşturur
    
    Args:
        rows: Satır sayısı
        cols: Sütun sayısı
        occupancy_rate: Dolu park yeri oranı (0-1 arası)
    """
    # Önce tüm alanı boş park yeri olarak başlat
    parking_lot = np.zeros((rows, cols), dtype=int)
    
    # Yolları yerleştir (her 3 sırada bir yatay, her 3 sütunda bir dikey yol)
    # Yatay yollar
    for i in range(2, rows, 3):
        if i < rows:
            parking_lot[i, :] = 2
    
    # Dikey yollar
    for j in range(2, cols, 3):
        if j < cols:
            parking_lot[:, j] = 2
    
    # Rastgele park yerlerini doldur
    empty_spots = [(i, j) for i in range(rows) for j in range(cols) 
                  if parking_lot[i, j] == 0]
    spots_to_fill = int(len(empty_spots) * occupancy_rate)
    
    filled_spots = random.sample(empty_spots, spots_to_fill)
    for spot in filled_spots:
        parking_lot[spot] = 1
    
    return parking_lot

def find_valid_start_positions(parking_lot):
    """Geçerli başlangıç noktalarını bulur (yol üzerinde olan noktalar)"""
    rows, cols = parking_lot.shape
    valid_positions = []
    
    # Alt kenarı kontrol et
    for j in range(cols):
        if parking_lot[rows-1, j] == 2:
            valid_positions.append((rows-1, j))
    
    # Sol kenarı kontrol et
    for i in range(rows):
        if parking_lot[i, 0] == 2:
            valid_positions.append((i, 0))
    
    return valid_positions

def main():
    app = QApplication(sys.argv)
    
    parking_lot = create_parking_lot(rows=9, cols=9, occupancy_rate=0.3)
    valid_starts = find_valid_start_positions(parking_lot)
    
    if not valid_starts:
        print("Uygun başlangıç noktası bulunamadı!")
        return
    
    start_pos = random.choice(valid_starts)
    
    algorithm = ParkingAlgorithm(parking_lot)
    best_spot, path = algorithm.find_best_spot(start_pos)
    
    window = ParkingLotWindow()
    window.parking_lot_view.update_data(parking_lot, start_pos, best_spot)
    window.update_directions(path)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
