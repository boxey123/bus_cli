import csv
import urllib.error
from urllib.request import Request, urlopen

atco_area_codes = [
    "620",  # Edinburgh
    "627",  # East Lothian
    "628",  # Midlothian
    "629"   # West Lothian
]

def main():
    data = []

    for area_code in atco_area_codes:
        url = f"https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv&atcoAreaCodes={area_code}"
        req = Request(url)
        req.add_header("Accept", "text/csv")

        try:
            with urlopen(req) as response:
                reader = csv.DictReader(response.read().decode().splitlines())
                for row in reader:
                    data.append(row)
        except urllib.error.URLError as e:
            print(f"Error fetching data for area code {area_code}: {e}")
            print("Aborting the process.")
            return

    with open("naptan_dataset.csv", "w", newline="") as csvfile:
        fieldnames = ["ATCOCode", "NaptanCode", "PlateCode", "CleardownCode", "CommonName", "CommonNameLang", "ShortCommonName", "ShortCommonNameLang", "Landmark", "LandmarkLang", "Street", "StreetLang", "Crossing", "CrossingLang", "Indicator", "IndicatorLang", "Bearing", "NptgLocalityCode", "LocalityName", "ParentLocalityName", "GrandParentLocalityName", "Town", "TownLang", "Suburb", "SuburbLang", "LocalityCentre", "GridType", "Easting", "Northing", "Longitude", "Latitude", "StopType", "BusStopType", "TimingStatus", "DefaultWaitTime", "Notes", "NotesLang", "AdministrativeAreaCode", "CreationDateTime", "ModificationDateTime", "RevisionNumber", "Modification", "Status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    main()