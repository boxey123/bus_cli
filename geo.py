import math
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float

@dataclass(frozen=True)
class BoundingBox:
    ne: Coordinate  # North east
    sw: Coordinate  # South west

def bounding_box(centre: Coordinate, radius: float) -> BoundingBox:
    latitude  = centre.latitude
    longitude = centre.longitude

    # Approximate conversion from meters to degrees latitude
    lat_offset  = radius / 111_000 
    # Approximate conversion from meters to degrees longitude, adjusted for latitude
    long_offset = radius / (111_000 * abs(math.cos(math.radians(latitude))))

    ne_lat  = latitude  + lat_offset
    ne_long = longitude + long_offset
    sw_lat  = latitude  - lat_offset
    sw_long = longitude - long_offset

    logger.debug("Postcode coordinates: (%.6f, %.6f)", latitude, longitude)
    logger.debug("NE: (%.6f, %.6f) SW: (%.6f, %.6f)", ne_lat, ne_long, sw_lat, sw_long)

    return BoundingBox(
        ne=Coordinate(ne_lat, ne_long),
        sw=Coordinate(sw_lat, sw_long)
    )

def haversine_distance(coord1: Coordinate, coord2: Coordinate) -> float:
    R = 6_371_000  # Radius of the Earth in meters

    lat_1   = coord1.latitude
    long_1  = coord1.longitude
    lat_2   = coord2.latitude
    long_2  = coord2.longitude

    lat1_rad    = math.radians(lat_1)
    lat2_rad    = math.radians(lat_2)
    long1_rad   = math.radians(long_1)
    long2_rad   = math.radians(long_2)

    delta_lat   = lat2_rad  - lat1_rad
    delta_long  = long2_rad - long1_rad
    
    a = (math.sin(delta_lat / 2) ** 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(delta_long / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    logger.info("Calculated Haversine distance between (%.6f, %.6f) and (%.6f, %.6f): %.2f meters", lat_1, long_1, lat_2, long_2, distance)
    logger.debug("Delta Latitude: %g, Delta Longitude: %g, a: %g, c: %g", delta_lat, delta_long, a, c)
    return distance