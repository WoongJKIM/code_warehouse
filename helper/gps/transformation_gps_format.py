#좌표 형태를 바꿔줌 네이버나 국가는 tm128방식을 사용하는데 이것을 우리가 아는 gps 좌표계로 변경할 수 있음
from pyproj import Proj
from pyproj import transform

WGS84 = {
    'proj':'latlong', 
    'datum':'WGS84', 
    'ellps':'WGS84', 
}

TM128 = { 
    'proj':'tmerc', 
    'lat_0':'38N', 
    'lon_0':'128E',
    'ellps':'bessel',
    'x_0':'400000',
    'y_0':'600000',
    'k':'0.9999',
    'towgs84':'-146.43,507.89,681.46',
}

GRS80 = {
    'proj' : 'tmerc', 
    'lat_0' : '38N', 
    'lon_0' : '127.5E', 
    'k' : '0.9996', 
    'x_0' : '1000000', 
    'y_0' : '2000000', 
    'ellps' : 'GRS80', 
    'units' : 'm',
}

TM127 = {
    'proj' : 'tmerc', 
    'lat_0' : '38N', 
    'lon_0' : '127.0028902777777777776E', 
    'ellps' : 'bessel', 
    'x_0' : '200000', 
    'y_0' : '500000', 
    'k' : '1.0', 
    'towgs84' : '-146.43,507.89,681.46',
}

class transformationGpsFormat:
    def __init__(self):
        pass
    
    def tm127_to_wgs84(self, row):
        return transform(Proj(**TM127), Proj(**WGS84), row['mapx'] / 2.5, row['mapy'] / 2.5 )
    
    #네이버의 좌표 저장 방식을 gps 좌표로 변경
    def tm128_to_wgs84(self, row):
    
        return transform(Proj(**TM128), Proj(**WGS84), row['mapx'], row['mapy'])
    
    # UTM-K
    def grs80_to_wgs84(self, row):
        
        return transform(Proj(**GRS80), Proj(**WGS84), row['mapx'], row['mapy'] )
    
    def wgs84_to_tm128(self, row):
        lon, lat = transform(Proj(**WGS84), Proj(**TM128), row['lng'], row['lat'])
        return lat, lon

    def wgs84_to_tm127(self, row):
        lon, lat = map(lambda x:2.5*x, transform(Proj(**WGS84), Proj(**TM127), row['lng'], row['lat']))
        return lat, lon