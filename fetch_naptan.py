import csv
from urllib.request import Request, urlopen

atco_area_codes = [
    "620",  # Edinburgh
    "627",  # East Lothian
    "628",  # Midlothian
    "629"   # West Lothian
]

with open("naptan_dataset.csv", "w", newline="") as csvfile:
    fieldnames = ["ATCOCode", "NaptanCode", "PlateCode", "CleardownCode", "CommonName", "CommonNameLang", "ShortCommonName", "ShortCommonNameLang", "Landmark", "LandmarkLang", "Street", "StreetLang", "Crossing", "CrossingLang", "Indicator", "IndicatorLang", "Bearing", "NptgLocalityCode", "LocalityName", "ParentLocalityName", "GrandParentLocalityName", "Town", "TownLang", "Suburb", "SuburbLang", "LocalityCentre", "GridType", "Easting", "Northing", "Longitude", "Latitude", "StopType", "BusStopType", "TimingStatus", "DefaultWaitTime", "Notes", "NotesLang", "AdministrativeAreaCode", "CreationDateTime", "ModificationDateTime", "RevisionNumber", "Modification", "Status"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for area_code in atco_area_codes:
        url = f"https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv&atcoAreaCodes={area_code}"
        req = Request(url)
        req.add_header("Accept", "text/csv")

        with urlopen(req) as response:
            reader = csv.DictReader(response.read().decode().splitlines())
            for row in reader:
                writer.writerow({
                    "ATCOCode": row["ATCOCode"] or "",
                    "NaptanCode": row["NaptanCode"] or "",
                    "PlateCode": row["PlateCode"] or "",
                    "CleardownCode": row["CleardownCode"] or "",
                    "CommonName": row["CommonName"] or "",
                    "CommonNameLang": row["CommonNameLang"] or "",
                    "ShortCommonName": row["ShortCommonName"] or "",
                    "ShortCommonNameLang": row["ShortCommonNameLang"] or "",
                    "Landmark": row["Landmark"] or "",
                    "LandmarkLang": row["LandmarkLang"] or "",
                    "Street": row["Street"] or "",
                    "StreetLang": row["StreetLang"] or "",
                    "Crossing": row["Crossing"] or "",
                    "CrossingLang": row["CrossingLang"] or "",
                    "Indicator": row["Indicator"] or "",
                    "IndicatorLang": row["IndicatorLang"] or "",
                    "Bearing": row["Bearing"] or "",
                    "NptgLocalityCode": row["NptgLocalityCode"] or "",
                    "LocalityName": row["LocalityName"] or "",
                    "ParentLocalityName": row["ParentLocalityName"] or "",
                    "GrandParentLocalityName": row["GrandParentLocalityName"] or "",
                    "Town": row["Town"] or "",
                    "TownLang": row["TownLang"] or "",
                    "Suburb": row["Suburb"] or "",
                    "SuburbLang": row["SuburbLang"] or "",
                    "LocalityCentre": row["LocalityCentre"] or "",
                    "GridType": row["GridType"] or "",
                    "Easting": row["Easting"] or "",
                    "Northing": row["Northing"] or "",
                    "Longitude": row["Longitude"] or "",
                    "Latitude": row["Latitude"] or "",
                    "StopType": row["StopType"] or "",
                    "BusStopType": row["BusStopType"] or "",
                    "TimingStatus": row["TimingStatus"] or "",
                    "DefaultWaitTime": row["DefaultWaitTime"] or "",
                    "Notes": row["Notes"] or "",
                    "NotesLang": row["NotesLang"] or "",
                    "AdministrativeAreaCode": row["AdministrativeAreaCode"] or "",
                    "CreationDateTime": row["CreationDateTime"] or "",
                    "ModificationDateTime": row["ModificationDateTime"] or "",
                    "RevisionNumber": row["RevisionNumber"] or "",
                    "Modification": row["Modification"] or "",
                    "Status": row["Status"] or ""
                })