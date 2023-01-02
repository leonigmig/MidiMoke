class Tempo:
    def __init__(self, bpm: int):
        self.bpm = bpm
        
    def get_beat_duration(self) -> float:
        return 60.0 / self.bpm
    
    def set_bpm(self, bpm: int):
        self.bpm = bpm