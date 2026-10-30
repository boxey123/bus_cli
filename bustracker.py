import json
import logging
import urllib.parse
import urllib.error
import datetime as dt
from dataclasses import dataclass
from geo import BoundingBox
from urllib.request import Request, urlopen

BASE_URL = "https://apim-public.trapezegroupazure.co.uk/edinburgh-cec-openapi/generic/v1.2/"

logger = logging.getLogger(__name__)

@dataclass
class ServiceDetail:
    publicservicename: str | None
    operator: str | None
    serviceRef: str | None

@dataclass
class areaobject:
    type: str | None
    id: str | None
    name: str | None
    options: dict | None
    latitude: float | None
    longitude: float | None
    operator: str | None
    publicservicename: str | None
    delay: int | None

@dataclass
class stoptimetableevent:
    operator: str | None
    publicservicename: str | None
    destination: str | None
    schedulearrivaltime: str | None
    scheduledeparturetime: str | None

class BusTrackerClientError(Exception):
    pass

class BusTrackerClient:
    def __init__(self, primary_key, secondary_key=None, timeout=10, base_url=BASE_URL):
        if not primary_key:
            raise ValueError("Primary API key is required.")

        self.primary_key    = primary_key
        self.secondary_key  = secondary_key
        self.base_url       = base_url
        self.timeout        = timeout
        logger.info("BusTrackerClient initialized with provided API keys.")

    def area_search(self, bounding_box: BoundingBox) -> list[dict]:
        params = {
            "ne_lat":   bounding_box.ne.latitude,
            "ne_long":  bounding_box.ne.longitude,
            "sw_lat":   bounding_box.sw.latitude,
            "sw_long":  bounding_box.sw.longitude
        }
        url = f"{self.base_url}AreaSearch?{urllib.parse.urlencode(params)}"
        req = Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Ocp-Apim-Subscription-Key", self.primary_key)

        try:
            with urlopen(req, timeout=self.timeout) as response:
                try:
                    data = json.loads(response.read().decode())
                    items = data.get("items", [])
                    logger.info("Area search returned %d items.", len(items))
                    return [
                        areaobject(
                                type = item.get("type", None),
                                id = item.get("id", None),
                                name = item.get("name", None),
                                options = item.get("options", None),
                                latitude = item.get("latitude", None),
                                longitude = item.get("longitude", None),
                                operator = item.get("operator", None),
                                publicservicename = item.get("publicservicename", None),
                                delay = item.get("delay", None)
                        ) for item in items
                    ]
                except (json.JSONDecodeError, KeyError) as e:
                    logger.error("Error processing response: %s", e)
                    raise BusTrackerClientError("Error processing response from API.") from e

        except urllib.error.HTTPError as e:
            logger.error("HTTP Error: %s - %s", e.code, e.reason)
            raise BusTrackerClientError(f"HTTP Error: {e.code} - {e.reason}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            logger.error("URL Error: %s", e)
            raise BusTrackerClientError(f"URL Error: {e}") from e

    def get_stop_timetable(self, stop_id: str):
        params = {
            "date": dt.datetime.now().strftime("%Y-%m-%d"),
            "atcocode": stop_id
        }

        url = f"{self.base_url}timetables/GetStopTimetable?{urllib.parse.urlencode(params)}"
        req = Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Ocp-Apim-Subscription-Key", self.primary_key)

        try:
            with urlopen(req, timeout=self.timeout) as response:
                try:
                    # There is an issue here where the API sometimes returns a 200 OK status but the body is not valid JSON.
                    data = json.loads(response.read().decode())
                    events = data.get("events", [])
                    logger.info("Timetable for stop %s returned %d events.", stop_id, len(events))
                    return [
                        stoptimetableevent(
                            operator=event.get("operator", None),
                            publicservicename=event.get("publicservicename", None),
                            destination=event.get("destination", None),
                            schedulearrivaltime=event.get("schedulearrivaltime", None),
                            scheduledeparturetime=event.get("scheduledeparturetime", None)
                        ) for event in events
                    ]
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    logger.error("Error processing response: %s", e)
                    raise BusTrackerClientError("Error processing response from API.") from e
        except urllib.error.HTTPError as e:
            logger.error("HTTP Error: %s - %s", e.code, e.reason)
            raise BusTrackerClientError(f"HTTP Error: {e.code} - {e.reason}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            logger.error("URL Error: %s", e)
            raise BusTrackerClientError(f"URL Error: {e}") from e

    # { "services": [{ "service": string, "operator": string, "serviceRef": string }]} not required
    def get_stop_services(
            self, 
            stop_id: str, 
            sms_code: bool = False, 
            from_date: dt.datetime | None = None, 
            to_date: dt.datetime | None = None
        ) -> list[ServiceDetail]:
        params = {
            "atcocode": stop_id,
            "smscode": "true" if sms_code else "false",
            "fromdate": from_date.strftime("%Y-%m-%d") if from_date else dt.datetime.now().strftime("%Y-%m-%d"),
            "todate": to_date.strftime("%Y-%m-%d") if to_date else dt.datetime.now().strftime("%Y-%m-%d")
        }

        url = f"{self.base_url}services/GetStopServices?{urllib.parse.urlencode(params)}"
        req = Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Ocp-Apim-Subscription-Key", self.primary_key)

        try:
            with urlopen(req, timeout=self.timeout) as response:
                logger.debug("Response status: %s", response.status)
                try:
                    decoded_response = response.read().decode()
                    logger.debug("Response length: %d : %s", len(decoded_response), decoded_response)
                    if not decoded_response:
                        logger.warning("Empty response body for stop %s.", stop_id)
                        return []
                    data = json.loads(decoded_response)
                    services = data.get("services", [])
                    logger.info("Services for stop %s returned %d services.", stop_id, len(services))
                    return [
                        ServiceDetail(
                            publicservicename=service.get("publicservicename", None),
                            operator=service.get("operator", None),
                            serviceRef=service.get("serviceRef", None)
                        ) for service in services
                    ]
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    logger.error("Error processing response: %s", e)
                    raise BusTrackerClientError("Error processing response from API.") from e
        except urllib.error.HTTPError as e:
            logger.error("HTTP Error: %s - %s", e.code, e.reason)
            raise BusTrackerClientError(f"HTTP Error: {e.code} - {e.reason}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            logger.error("URL Error: %s", e)
            raise BusTrackerClientError(f"URL Error: {e}") from e