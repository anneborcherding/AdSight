import json
import math

import pandas as pd

long_side = 0.0001
short_side = 0.00002

df = pd.read_csv('../data/billboard_data.csv')
billboards = df.groupby('billboard_name', as_index=False).first()
rectangles = []
for i in range(len(billboards)):
    lat_center = billboards.iloc[i]['latitude']
    lon_center = billboards.iloc[i]['longitude']
    rotation_radians = billboards.iloc[i]['rotation']/360*2*math.pi
    billboard_name = billboards.iloc[i]['billboard_name']
    first_point_x = lon_center+short_side*math.sin(rotation_radians)/2 - long_side*math.cos(rotation_radians)/2
    first_point_y = lat_center-short_side*math.cos(rotation_radians)/2 - long_side*math.sin(rotation_radians)/2

    second_point_x = first_point_x-short_side*math.sin(rotation_radians)*3/2
    second_point_y = first_point_y+short_side*math.cos(rotation_radians)

    third_point_x = second_point_x+long_side*math.cos(rotation_radians)*3/2
    third_point_y = second_point_y+long_side*math.sin(rotation_radians)

    forth_point_x = third_point_x+short_side*math.sin(rotation_radians)*3/2
    forth_point_y = third_point_y-short_side*math.cos(rotation_radians)

    rectangle = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [first_point_x, first_point_y],
                [second_point_x, second_point_y],
                [third_point_x, third_point_y],
                [forth_point_x, forth_point_y],
                [first_point_x, first_point_y]
            ]]
        },
        "properties": {
            "id": i,
            "name": billboard_name
        }
    }
    rectangles.append(rectangle)
geojson_data = {
    "type": "FeatureCollection",
    "features": rectangles
}

# Print the GeoJSON data
with open("../data/billboards.geojson", "w") as file:
    file.write(json.dumps(geojson_data, indent=2))
