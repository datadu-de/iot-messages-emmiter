# <https://gis.stackexchange.com/questions/164005/getting-random-coordinates-based-on-country>

import os
import random
import re

import shapefile
from dotenv import load_dotenv
from shapely.geometry import Point, shape

load_dotenv()


SHP_LOCATION = os.getenv(
    "SHP_LOCATION", "./assets/country_shapes/ne_10m_admin_0_countries.shp"
)
COUNTRY_NAME = os.getenv("COUNTRY_NAME", "Germany")


shapes = shapefile.Reader(SHP_LOCATION)  # reading shapefile with pyshp library
country = [s for s in shapes.records() if COUNTRY_NAME in s][
    0
]  # getting feature(s) that match the country name
country_id = int(
    re.findall(r"\d+", str(country))[0]
)  # getting feature(s)'s id of that match

shapeRecs = shapes.shapeRecords()
feature = shapeRecs[country_id].shape.__geo_interface__

shp_geom = shape(feature)

minx, miny, maxx, maxy = shp_geom.bounds


def random_coords_in_country():
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if shp_geom.contains(p):
            return {"lat": p.y, "lng": p.x}


for i in range(10):
    print(random_coords_in_country())
