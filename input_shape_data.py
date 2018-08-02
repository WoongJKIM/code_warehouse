import pandas as pd
import numpy as np
import pyproj
import geopandas as gp
import json

from pyproj import Proj
from pyproj import transform

from shapely.geometry import Point, LineString, Polygon

import os
import sys

import mongo_db

WGS84 = { 
    'proj':'latlong', 
    'datum':'WGS84', 
    'ellps':'WGS84' 
}

TM128 = { 
    'proj':'tmerc', 
    'lat_0':'38N', 
    'lon_0':'128E',
    'ellps':'bessel',
    'x_0':'400000',
    'y_0':'600000',
    'k':'0.9999',
    'towgs84':'-146.43,507.89,681.46'
}

GRS80 = {
    'proj' : 'tmerc', 
    'lat_0' : '38N', 
    'lon_0' : '127.5E', 
    'k' : '0.9996', 
    'x_0' : '1000000', 
    'y_0' : '2000000', 
    'ellps' : 'GRS80', 
    'units' : 'm' 
}

#좌표를 다른 방식에서 gps 방식으로 변경
#데이터 저장(네이버)
def point_tm128_to_wgs84(coordinates):
    
    return transform(Proj(**TM128), Proj(**WGS84), coordinates[0], coordinates[1])

#데이터 저장(국가 정보)
def point_grs80_to_wgs84(coordinates):
    
    return transform(Proj(**GRS80), Proj(**WGS84), coordinates[0], coordinates[1])

#경도 위도 순으로 표시되는 좌표를 folium 에서 사용할려면 위도 경도 순으로 변경해 저장해줘야 됨 바꾸는 것도 포함됨
def polygon_grs80_to_wgs84(polygon_grs80):
    coordinates_wgs84 = []
    polygon_wgs84 = []
    polygon_type = ""
    
    
    if polygon_grs80.geom_type == "Polygon":
        
        polygon_type = "Polygon"
        
        polygon_length = len(polygon_grs80.exterior.coords)
        polygon_index = 0
        
        for coordinate_grs in polygon_grs80.exterior.coords:
            coordinate_wgs = point_grs80_to_wgs84(coordinate_grs)
            
            if (coordinate_wgs in coordinates_wgs84) & (polygon_index < (polygon_length -1)):
                pass
            
            elif (polygon_index == (polygon_length - 1)):
                if (coordinates_wgs84[0] != coordinate_wgs):
                    coordinates_wgs84.append(coordinate_wgs)
                    coordinates_wgs84.append(coordinates_wgs84[0])
                    
                else:
                    coordinates_wgs84.append(coordinate_wgs)
            
            else :
                coordinates_wgs84.append(coordinate_wgs)
                
            polygon_index += 1
            
        polygon_wgs84.append(coordinates_wgs84)
        
    else :
        
        polygon_type = "MultiPolygon"
        
        for sub_polygon_grs80 in polygon_grs80:
            
            coordinates_wgs84 = []
            
            polygon_length = len(sub_polygon_grs80.exterior.coords)
            polygon_index = 0
            
            for coordinate_grs in sub_polygon_grs80.exterior.coords:
                coordinate_wgs = point_grs80_to_wgs84(coordinate_grs)
                
                if (coordinate_wgs in coordinates_wgs84) & (polygon_index < (polygon_length -1)):
                    pass
                
                elif (polygon_index == (polygon_length - 1)):
                    if (coordinates_wgs84[0] != coordinate_wgs):
                        coordinates_wgs84.append(coordinate_wgs)
                        coordinates_wgs84.append(coordinates_wgs84[0])
                        
                    else :
                        coordinates_wgs84.append(coordinate_wgs)

                else :
                    coordinates_wgs84.append(coordinate_wgs)
                    
                polygon_index += 1
                
                #multi_polygon.append(coordinate_wgs)
            polygon_wgs84.append(coordinates_wgs84)  

    return polygon_type, polygon_wgs84

def set_shape_df():
    shape_df=gp.GeoDataFrame.from_file('주소 정보 폴더/BND_TOTAL_OA_PG.shp', encoding='euc-kr')
    
    shape_df['TOT_OA_CD'] = shape_df['TOT_OA_CD'].apply(lambda x : int(x))
    shape_df['ADM_DR_CD'] = shape_df['ADM_DR_CD'].apply(lambda x : int(x))
    
    region_df = pd.read_excel("주소 정보 폴더/region_code_sigungu_2014.xlsx")
    region_df['region_code'] = region_df['region_code'].apply(lambda x : int(x))
    
    shape_df = shape_df.merge(region_df, how = 'inner', left_on = ['ADM_DR_CD'], right_on = ['region_code'])
    
    shape_df.drop(['ADM_DR_CD','OBJECTID'], axis = 1, inplace = True)
    
    return shape_df

def input_shape_data_into_db(shape_df):
    
    analysis_con = mongo_db#몽고 콘
    shape_TOT_table = analysis_con.shapeTOT
    
    bulk = shape_TOT_table.initialize_ordered_bulk_op()
    
    shape_columns = list(shape_df.columns)
    
    for idx, row in shape_df.iterrows():
        
        geometry_wgs84 = polygon_grs80_to_wgs84(row["geometry"])
        
        geometry_type = geometry_wgs84[0]
        geometry_polygons = geometry_wgs84[1]
        
        MultiPolygon_num = 0
        
        #멀티폴리곤 일 경우 폴리곤 하나씩 따로 저장 (이유 : 인덱스가 안먹음)
        for geometry_polygon in geometry_polygons:
            shape_dict = {}
        
            shape_dict['type'] = "Feature"
                
            for column in shape_columns:
                if column == "geometry":
                    geometry_wgs84 = polygon_grs80_to_wgs84(row["geometry"])
                    shape_dict[column] = {
                        "type" : "Polygon",
                        "coordinates" : [geometry_polygon]
                    }
                elif column == "region_code":
                    shape_dict["properties"] = {column : row[column]}
                elif column == "_id":
                    pass
                else:
                    shape_dict[column] = row[column]

            else:
                pass

            bulk.insert(shape_dict)       
        
    result = bulk.execute()
    
    return result