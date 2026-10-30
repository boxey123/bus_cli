import os
import logging
from geo import bounding_box
from naptan import load_naptan
from dotenv import load_dotenv
from stops import find_nearby_stops, Service
from postcode import fetch_coordinate, PostcodeLookupError
from bustracker import BusTrackerClient, BusTrackerClientError

LOGGING_LEVEL       = logging.WARNING   # Use logging.DEBUG when troubleshooting 
LOGGING_FILE_MODE   = "w"               # a = append, w = overwrite
MAXIMUM_RADIUS      = 1000.0            # Maximum radius in meters

logger = logging.getLogger(__name__)

def get_api_keys() -> dict:
    logger.info("Retrieving API keys from environment variables.")

    primary_key = os.getenv("BUSTRACKER_PRIMARY_KEY")
    secondary_key = os.getenv("BUSTRACKER_SECONDARY_KEY")
    
    return { "primary": primary_key, "secondary": secondary_key }

def ask_postcode() -> str:
    while True:
        postcode = input("Enter a postcode: ").strip().upper()
        if postcode:
            logger.debug("User entered postcode: %s", postcode)
            return postcode

        print("No postcode entered. Please try again.")

def ask_radius() -> float:
    while True:
        try:
            radius = float(input("Enter a radius in meters: ").strip())
            if 0.0 < radius <= MAXIMUM_RADIUS:
                logger.debug("User entered radius: %.2f meters", radius)
                return radius
            else:
                print(f"Radius must be between 0 and {MAXIMUM_RADIUS} meters. Please try again.")
        except ValueError:
            print("Invalid input for radius. Please enter a numeric value.")

def main():
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("bus_app.log", mode=LOGGING_FILE_MODE),
            logging.StreamHandler()
        ]
    )
    load_dotenv()
    api_keys = get_api_keys()

    if not api_keys["primary"] or not api_keys["secondary"]:
        logger.error("API keys not found in environment variables.")
        print("Error: API keys not found. Please set BUSTRACKER_PRIMARY_KEY and BUSTRACKER_SECONDARY_KEY in your environment.")
        return

    client = BusTrackerClient(primary_key=api_keys["primary"], secondary_key=api_keys["secondary"])

    try:
        naptan_data = load_naptan()
    except (FileNotFoundError, KeyError) as e:
        logger.error("Error loading NaPTAN data: %s", e)
        print("Error: could not load 'naptan_dataset.csv'. Run fetch_naptan.py or check the file.")
        return

    if not naptan_data:
        logger.error("Failed to load NaPTAN data.")
        print("Error: Failed to load NaPTAN data. Please ensure 'naptan_dataset.csv' is present and correctly formatted.")
        return

    postcode_in = ask_postcode()
    try: 
        postcode_coord = fetch_coordinate(postcode_in)
    except PostcodeLookupError as e:
        print(e)
        return

    radius_in = ask_radius()

    search_box = bounding_box(postcode_coord, radius_in)
    try: 
        search_result = client.area_search(search_box)
    except BusTrackerClientError as e:
        print(e)
        return

    nearby_stops = find_nearby_stops(postcode_coord, radius_in, search_result, naptan_data)

    if not nearby_stops:
        print(f"No bus stops found within {radius_in} meters of postcode {postcode_in}.")
        return

    stop_services = {}

    for stop in nearby_stops:
        stop_services[stop.id] = []
        try:
            services = client.get_stop_services(stop.id)
        except BusTrackerClientError as e:
            logger.error("Error retrieving services for stop %s: %s", stop.label, e)
            print(f"Error retrieving services for stop {stop.label}: {e}")
            continue

        try: 
            for service in services:
                stop_services[stop.id].append(Service(
                    public_name=service.publicservicename,
                    operator=service.operator,
                    service_reference=service.serviceRef
                ))
        except KeyError as e:
            logger.error("Missing expected service data for stop %s: %s", stop.label, e)
            print(f"Error processing services for stop {stop.label}: Missing expected data.")
            continue
    
    for stop in nearby_stops:
        services = stop_services.get(stop.id)

        if not services:
            logger.info("No services found for stop %s.", stop.label)
            print(f"\nNo services found for stop {stop.label}.")
            continue

        print(f"\nServices for {stop.label}")
        for service in services:
            print(f"  Service Name: {service.public_name}, Operator: {service.operator}, Service Reference: {service.service_reference}")

    print("\nBus stop locations: Data provided by City of Edinburgh Council")
        
if __name__ == "__main__":
    main()