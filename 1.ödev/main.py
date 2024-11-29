from gui.parking_visualizer import visualize_parking_lot_qt
import cProfile
import pstats

def profile_app():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Ana uygulamayı çalıştır
    visualize_parking_lot_qt()
    
    profiler.disable()
    
    # Sonuçları kaydet
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.dump_stats('new_profile.prof')

if __name__ == "__main__":
    profile_app()
