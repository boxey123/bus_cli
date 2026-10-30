import logging
from naptan import NaPTANStop
from dataclasses import dataclass
from bustracker import areaobject
from geo import Coordinate, haversine_distance

logger = logging.getLogger(__name__)

BUS_STOP_TYPES = {
    "BCT",
    "BCS",
}

@dataclass
class Stop:
    name: str
    id: str
    distance: float
    latitude: float
    longitude: float
    stop_type: str
    bearing: str | None
    bus_stop_type: str | None

    @property
    def label(self) -> str:
        if self.bearing:
            return f"{self.name} ({self.bearing})"
        else:
            return self.name

@dataclass
class Service:
    public_name: str
    operator: str
    service_reference: str

def find_nearby_stops(
        centre: Coordinate, 
        radius: float, 
        items: list[areaobject], 
        naptan: dict[str, NaPTANStop]
) -> list[Stop]:
    stops = []

    for stop in items:
        if stop.type != "STOP":
            continue

        stops.append(stop)

    stops_filtered = []

    for stop in stops:
        lat    = stop.latitude
        long   = stop.longitude
        stop_coord = Coordinate(latitude=lat, longitude=long)
        distance = haversine_distance(centre, stop_coord)

        if distance <= radius:
            naptan_stop = naptan.get(stop.id)

            if not naptan_stop:
                logger.debug("NaPTAN data not found for stop %s (%s). Skipping.", stop.name, stop.id)
                continue

            if naptan_stop.stop_type not in BUS_STOP_TYPES:
                logger.debug("Stop %s is not a bus stop. Skipping.", stop.name)
                continue

            if naptan_stop.status != "active":
                logger.debug("Stop %s is not active. Skipping.", stop.name)
                continue

            stops_filtered.append(Stop(
                name=stop.name,
                id=stop.id,
                distance=distance,
                latitude=lat,
                longitude=long,
                stop_type=naptan_stop.stop_type,
                bearing=naptan_stop.bearing,
                bus_stop_type=naptan_stop.bus_stop_type
            ))
            logger.debug("Stop %s (atcocode: %s) is %.2f meters away, which is within the radius of %.2f meters.", stop.name, stop.id, distance, radius)
        else:
            logger.debug("Stop %s (atcocode: %s) is %.2f meters away, which is outside the radius of %.2f meters.", stop.name, stop.id, distance, radius)


    stops_filtered.sort(key=lambda x: x.distance)
    return stops_filtered