import json
import logging
import urllib.parse
import urllib.error
from geo import Coordinate
from urllib.request import Request, urlopen

BASE_URL = "https://api.postcodes.io/scotland/postcodes/"

logger = logging.getLogger(__name__)

class PostcodeLookupError(Exception):
    pass

def fetch_coordinate(postcode: str, timeout: int = 10) -> Coordinate:
    url = f"{BASE_URL}{urllib.parse.quote(postcode)}"

    req = Request(url)
    req.add_header("Accept", "application/json")

    try: 
        with urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            latitude = data['result']['latitude']
            longitude = data['result']['longitude']
            logger.debug("Fetched coordinates for postcode %s: (%.6f, %.6f)", postcode, latitude, longitude)
            return Coordinate(latitude, longitude)

    except urllib.error.HTTPError as e:
        raise PostcodeLookupError(f"HTTP Error: {e.code} - {e.reason}") from e
    except (urllib.error.URLError, TimeoutError) as e:
        raise PostcodeLookupError(f"URL Error: {e}") from e
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise PostcodeLookupError("Error processing response from API.") from e