from enum import Enum

class Rank(Enum):
    KLAS1 = 1
    KLAS2 = 2
    HAVO3 = 3
    HAVO4 = 4
    HAVO5 = 5
    VWO3 = 6
    VWO4 = 7
    VWO5 = 8
    VWO6 = 9
    DOCENT = 10
    RECTOR = 11
    MUTED = 0
    def __str__(self):
        return self.name
