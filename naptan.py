import csv
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class NaPTANStop:
    common_name: str
    atco_code: str
    stop_type: str
    status: str
    bearing: str | None
    bus_stop_type: str | None

def load_naptan(path: str = "naptan_dataset.csv") -> dict[str, NaPTANStop]:
    stops = {}

    with open(path, "r") as f:
        reader  = csv.DictReader(f)
        for row in reader:
            code = row["ATCOCode"]
            stops[code] = NaPTANStop(
                common_name=row["CommonName"],
                atco_code=row["ATCOCode"],
                stop_type=row["StopType"],
                status=row["Status"],
                bearing=(row["Bearing"] if row["Bearing"] else None),
                bus_stop_type=(row["BusStopType"] if row["BusStopType"] else None)
            )
            logger.debug("Loaded NaPTAN stop: %s with ATCOCode: %s", row["CommonName"], code)
    return stops