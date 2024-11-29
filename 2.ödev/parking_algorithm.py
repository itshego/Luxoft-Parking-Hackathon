from typing import Tuple, Optional
import numpy as np
from queue import PriorityQueue

class ParkingAlgorithm:
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.rows, self.cols = grid.shape
        
    def find_best_spot(self, start_pos: Tuple[int, int]) -> Tuple[Optional[Tuple[int, int]], list]:
        distances = np.full((self.rows, self.cols), np.inf)
        distances[start_pos] = 0
        pq = PriorityQueue()
        pq.put((0, start_pos))
        visited = set()
        # Her nokta için önceki noktayı takip et
        previous = {start_pos: None}
        
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        while not pq.empty():
            current_dist, current_pos = pq.get()
            
            if current_pos in visited:
                continue
                
            visited.add(current_pos)
            
            if self.grid[current_pos] == 0:
                # Yolu geri izle
                path = []
                current = current_pos
                while current is not None:
                    path.append(current)
                    current = previous.get(current)
                return current_pos, path[::-1]  # Yolu baştan sona sırala
            
            for dy, dx in directions:
                new_y = current_pos[0] + dy
                new_x = current_pos[1] + dx
                
                if 0 <= new_y < self.rows and 0 <= new_x < self.cols:
                    if self.is_valid_move(current_pos, (new_y, new_x)):
                        new_dist = current_dist + 1
                        if new_dist < distances[new_y, new_x]:
                            distances[new_y, new_x] = new_dist
                            previous[(new_y, new_x)] = current_pos
                            pq.put((new_dist, (new_y, new_x)))
        
        return None, []
    
    def is_valid_move(self, current_pos: Tuple[int, int], next_pos: Tuple[int, int]) -> bool:
        """Geçerli bir hareket mi kontrol eder"""
        # Yoldan geçiyor mu?
        if self.grid[next_pos] == 2:  # 2 yolu temsil eder
            return True
        # Boş park yerine gidiyor mu?
        if self.grid[next_pos] == 0:
            # Dikey giriş kontrolü
            return abs(next_pos[1] - current_pos[1]) == 0
        return False 