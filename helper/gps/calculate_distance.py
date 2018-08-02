import math

class getDistance:
    def __init__(self):
        pass
    
    #존 사이의 거리를 측정하는 함수(KM)
    #위도와 경도를 지정된 지표면 상의 두 점사이의 대원 거리를 계산.
    def set_distance_between_point(self, lat_lon1, lat_lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """

        lat1, lon1 = lat_lon1
        lat2, lon2 = lat_lon2

        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        km = 6367 * c
        return km